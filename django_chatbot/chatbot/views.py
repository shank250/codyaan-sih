from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
# from .models import Chat
from django.utils import timezone
import os
from langchain.memory import ChatMessageHistory
import pymongo

from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import json
chat_summary = ""
chat_summary_status = False

os.environ['OPENAI_API_KEY'] = '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'


history = ChatMessageHistory()
user_chat = []
ai_chat = []

# Create your views here.

openai_api_key = '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'
openai.api_key = openai_api_key

def complaint_mongodb():
    llm = ChatOpenAI(temperature=0.6)
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
    import pymongo
    from pymongo import MongoClient
    connection_string = "mongodb+srv://codyaanSIH:VEkE6wjohQ9v01De@cluster0.vkfifhe.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"

    # Replace these with your MongoDB Atlas connection details
    # connection_string = ""

    # Initialize the MongoDB client
    client = MongoClient(connection_string)

    # Select the database you want to use
    db = client['test']

    # Select the collection within the database
    collection = db['complaints']

    # Data to insert into the collection
    data_to_insert = dictionary_response
# tyoe refers catagory
    # Insert the data into the collection
    insert_result = collection.insert_one(data_to_insert)

    # Check if the insertion was successful
    if insert_result.acknowledged:
        print("Data inserted successfully. Inserted ID:", insert_result.inserted_id)
    else:
        print("Data insertion failed.")

    # Close the MongoDB connection
    client.close()


# now giving my chat description of the llm for vector search
def vector_search(chat_summary = chat_summary, user_chat = user_chat):
    import pymongo
    import json
    import time
    llm = ChatOpenAI(temperature=0.6)

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
  

    start_time = time.time()
    # Replace these with your MongoDB Atlas connection details
    mongo_uri = "mongodb+srv://codyaanSIH:VEkE6wjohQ9v01De@cluster0.vkfifhe.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    collection_name = "employees"

    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(mongo_uri)

    # Access the database and collection
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
        # print(document)
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
    # Close the MongoDB connection
    client.close()
    # print(documents)
    # print(metadatas)
    # print(ids)



    import chromadb

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




def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    print(response)
    answer = response.choices[0].message.content.strip()
    return answer


def chatbot(request):

    # return render(request, 'chatbot.html')
    # chats = Chat.objects.filter(user=request.user)
    # complaint_mongodb()

    if request.method == 'POST':
        user_query = request.POST.get('message')
        user_chat.append(user_query)
        history.add_user_message(user_query)

        global chat_summary
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain.chains import LLMChain
        import os

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
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain.chains import LLMChain
        llm = ChatOpenAI(temperature=0.6)
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
        
        # response = ask_openai(message)
        # response = "hi this my response."
        # print(response)
        # chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        # chat.save()
        if response == "[COMPLAINT-FILABLE]":
            status = "done"
            print("moving it to create a vector search prompt")
            vector_search()
            
        print("\n oopes trying to get more data")
        status = "more-data-req"
        print(response)
        # dictionary_response = json.loads(response)
        # response_ai = dictionary_response["chat-reply"]
        # user_query = input(dictionary_response["chat-reply"] + "\nuser : ")
        print("CHAT SUMmARY : " + chat_summary)
        # complaint_completion(str(history.messages) + user_query)
        return JsonResponse({'message': user_query, 'response': response})
    
    

    # elif response == "[IRRELEVANT]":
    #     print("not sure what you are talking about")
    #     status = "new-chat"
    # else:
    #     print("\n oopes trying to get more data")
    #     status = "more-data-req"
    #     # print(response)
    #     dictionary_response = json.loads(response)
    #     user_query = input(dictionary_response["chat-reply"] + "\nuser : ")
    #     print("CHAT SUMmARY : " + chat_summary)
    #     complaint_completion(str(history.messages) + user_query)

    return render(request, 'chatbot.html')





def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'chatbot.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'login.html')

from django.http import HttpResponse
from django.template import loader

def user_dash(request):
    template = loader.get_template('user_dash.html')
    return HttpResponse(template.render())

def profile(request):
    template = loader.get_template('profile.html')
    return HttpResponse(template.render())

def logout(request):
    auth.logout(request)
    return redirect('login')