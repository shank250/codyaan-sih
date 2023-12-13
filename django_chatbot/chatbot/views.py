import os
import json
import openai
import chromadb
import pymongo

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from .models import UserProfile

from pymongo import MongoClient

from langchain.memory import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

chat_summary = ""
chat_summary_status = False
os.environ['OPENAI_API_KEY'] = 'apikey'
history = ChatMessageHistory()
user_chat = []
ai_chat = []
openai_api_key = 'apikey'
openai.api_key = openai_api_key
llm = ChatOpenAI(temperature=0.6)


def complaint_mongodb():
    prompt = ChatPromptTemplate.from_template(
        """You are banking grivance complaint loger. 
        
        by using the chat history between ai and user gather all these informations in json formatted to \
        look like :
        {{{{
        "username": str / name of the user ,
        "employeeId" : str / employee email-id ,
        "userid": str / user email-id,
        "userLocation" : str / user location,
        "complaint" : str / give a full detailed report of the complaint of the user to the employee in 200 words,
        "status" : str / "pending" - allways,
        "type" : str / complain catagory from vector search query,
        "bank" : str / name of the bank from whom the complaint relate to,
        "documents" : [{{{{
            "documentName" : str / document to be uploaded ,
            "documentUrl" : "hello.com" - always
        }}}}]
        }}}}
        
        all chat summary : {chat}"""
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    chat = str(history.messages)
    complaint_dict_str = chain.run(chat)
    dictionary_response = json.loads(complaint_dict_str)
    dictionary_response["employeeId"] = "rajesh.yadav@gmail.com"
    print(dictionary_response)
    
    connection_string = "Enter your cluster string"
    client = MongoClient(connection_string)
    db = client['test']
    collection = db['complaints']

    data_to_insert = dictionary_response
    # Insert the data into the collection
    insert_result = collection.insert_one(data_to_insert)

    if insert_result.acknowledged:
        print("Data inserted successfully. Inserted ID:", insert_result.inserted_id)
    else:
        print("Data insertion failed.")
    client.close()


def vector_search(chat_summary = chat_summary, user_chat = user_chat):
    

    prompt = ChatPromptTemplate.from_template(
        """You are a grivance complaint registration bot\
        now create a best suitalbe json object with following fields : \
        'vector-search' = this key will contain a string which would be \
        vector search should contain bank name, type of the problem, problem catagory, languge in which user is talking location where the complaint belongs to. \
            here is the user detailed problem  : {summary}"""
    )
    summary = str(user_chat) + chat_summary
    print(summary)
    chain = LLMChain(llm=llm, prompt=prompt)
    vector_search_query = chain.run(summary)
    print(vector_search_query)
  
    mongo_uri = "enter your MongoDB cluster URL or connecting string"
    collection_name = "employees"
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database("test")
    collection = db[collection_name]

    # Query data from the collection
    query = {}  # You can specify a query here if needed
    result = collection.find(query)

    documents = []
    metadatas = []
    ids = []
    # Iterate over the results and print them
    for document in result:
        lang = str(document["language"])
        comp_specialisation = str(document["complaintSpecialisation"])
        emp_description = document["bankName"] + document["workplace"] + lang + comp_specialisation
        emp_metadata = document["name"]
        emp_ids = document["username"]
        documents.append(emp_description)
        meta_string = '{"source": "'+ emp_metadata+ '"}'
    #     meta data string contain the employee name
        meta_dict = json.loads(meta_string)
        metadatas.append(meta_dict)
        ids.append(emp_ids)
    client.close()

    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="my_bank_col")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    results = collection.query(
        query_texts=[vector_search_query],
        n_results=1
    )
    print(results)
    complaint_mongodb()
    return vector_search_query


def login(request):
    if request.method == 'POST':
        print("Request okay")
        global emailID
        email= request.POST['email']
        print(email)
        emailID=email
        password = request.POST['password1']
        context={
            'email': email,
        }

        client = MongoClient('mongodb://localhost:27017/')
        db = client['User_database']  
        users_collection = db['chatbot_userprofile']

        print('mongdb connected okay')
        user_document = users_collection.find_one({'email': email})
        if user_document:
            # user_data_str=user_document['username']
            # user_data_dict=user_data_str.replace('\'','\"')
            # username_json = json.loads(user_data_dict)
            # password2 = username_json['password2']
            # print(password2) 
            password2=user_document['password']
            if password==password2:
                print('Password matched')
                request.session['emailID'] = email
                return redirect('chatbot')
                # return render(request,'chatbot.html',context)
        else:
            error="Register"
            return render(request, 'register.html')
    return render(request, 'login.html') 


def profile(request):
    emailID = request.session.get('emailID', None)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['User_database']  
    users_collection = db['chatbot_userprofile']
    user_document = users_collection.find_one({'email': emailID})
    print(user_document['full_name'])
    context = {
        'full_name': user_document['full_name'],
        'user_id': user_document['public_id'],
        'mobile_number': user_document['mobile_number'],
        'email': user_document['email'],
        'password': '********',
        'aadhar_number': user_document['aadhar_number'], 
        'language': user_document['language'],
    }
    return render(request,'profile.html',context)


def chatbot(request):
    emailID = request.session.get('emailID', None)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['User_database']  
    users_collection = db['chatbot_userprofile']
    print(emailID)
    user_document = users_collection.find_one({'email': emailID})
    print(user_document)
    # print( user_document['full_name'])
    context = {
        'user_profile': user_document['full_name'],
    }   
    
    if request.method == 'POST':
        user_query = request.POST.get('message')
        user_chat.append(user_query)
        history.add_user_message(user_query)

        global chat_summary
        os.environ['OPENAI_API_KEY'] = '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'
        llm = ChatOpenAI(temperature=0.6)
        prompt = ChatPromptTemplate.from_template(
            """You are banking grivance complaint loger. 
            
            try to take as much as complaint inforamation possible.


            if you think for a given complaint you have collected these data \
            user name, bank name, transaction id (if required), cards details or any other details for that specific issue user is facing.
            then return [COMPLAINT-FILABLE]

            

            other wise ask user for all other required informations for solving that problem \
            Return JSON object formatted to look like :
            
            {{{{
                "chat-reply": string \ reply tobe send to the user telling about all the informations which are required\
                "facts" :   also add one more json object which \
                            store  important information or user in the form of json or dictionary for future reference which it gathers during converation.\
                            these data should be correct and precise
                "STATUS": string \ This should be "More info required"
            }}}}
            
            
            all chat with summary : {chat}"""
        )
        chain = LLMChain(llm=llm, prompt=prompt)

        response = chain.run(str(history.messages) + user_query)
        ai_chat.append(response)
        history.add_ai_message(response)
        print(response)

        # creating a chat summary
        prompt = ChatPromptTemplate.from_template(
            """Make a chat summary : \
            keeping all the facts correct and without missing any important information \
            
            also add one more json object which \
            store these important information or user in the form of json or dictionary for future reference. And update this dictionary with\
            the users chat and ai chat. this json object is added so that no information is missed.

            here is the complete chat. Make sure that you remember and write names and other details entered by the user in this summary : {chat}?"""
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        chat =  chat_summary + user_chat[-1] + ai_chat[-1]
        chat_summary = chain.run(chat)

        if response == "[COMPLAINT-FILABLE]":
            status = "done"
            print("moving it to create a vector search prompt")
            vector_search()
            
        print("\n oopes trying to get more data")
        status = "more-data-req"
        print(response)
        print("CHAT SUMmARY : " + chat_summary)
        return JsonResponse({'message': user_query, 'response': response})
    return render(request, 'chatbot.html', context)


def register(request):
    if request.method == 'POST':
        full_name = request.POST['username']
        public_id = request.POST['userID']
        mobile_number = request.POST['number']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']        
        aadhar_number = request.POST['aadharNo']
        language = request.POST['language']

        user = get_user_model().objects.create(username=full_name, password=password1)

        if password1 == password2:
            user_profile = UserProfile(
                user=user,
                full_name=full_name,
                public_id=public_id,
                mobile_number=mobile_number,
                email=email,
                password=password1,
                aadhar_number=aadhar_number,
                language=language
            )
            user_profile.save()
            # auth.login(request, user)
            request.session['emailID'] = email
            return redirect('chatbot') 
    return render(request, 'register.html')


def home(request):
    return render(request,'home.html')


def user_dash(request):
    template = loader.get_template('user_dash.html')
    return HttpResponse(template.render())


def logout(request):
    auth.logout(request)
    return redirect('login')





# def login(request):
#     if request.method == 'POST':
#         userID = request.POST['userID']
#         password1 = request.POST['password1']
#         user = auth.authenticate(request, userID=userID, password1=password1)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('chatbot')
#         else:
#             error_message = 'Invalid userID or password'
#             return render(request, 'login.html', {'error_message': error_message})
#     else:
#         return render(request, 'chatbot.html')





# def register(request):
#     if request.method == 'POST':
#         email= request.POST['email']
#         password1= request.POST['password1']
#         user_data = {
#             'username': request.POST['username'],
#             'userID': request.POST['userID'],
#             'password2': request.POST['password2'],
#             'aadharNo': request.POST['aadharNo'],
#             'mobileNo': request.POST['number'],
#             'language': request.POST['language'], 
#             }
#         if password1 == user_data['password2']:
#             # obj=User(
#             #     username = user_data['username'],
#             #     email = email,
#             #     password1 = password1,
#             #     password2 = password1,
#             #     userID = user_data['userID'],
#             #     aadharNo = user_data['aadharNo'],
#             #     phoneNo =user_data['mobileNo'],
#             #     language = user_data['language'],
#             # )
#             # obj.save()
#             user = User.objects.create_user(user_data, email, password1)
#             user.save()
#             auth.login(request, user)
#             return redirect('chatbot')
#     return render(request, 'register.html')
