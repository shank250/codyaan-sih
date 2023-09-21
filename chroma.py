import pymongo
import json
import time

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
    lang = str(document["Languages Spoken"])
    comp_specialisation = str(document["Complaint Specialization"])
    emp_description = document["Bank Name"] + document["Branch Name"] + lang + comp_specialisation
    emp_metadata = document["Name"]
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
    query_texts=["credit card solution in varansi in hindi"],
    n_results=2
)
print(results["documents"])


end_time = time.time()  # Record the time again after your code has executed
execution_time = end_time - start_time  # Calculate the execution time
print(f"Execution time: {execution_time} seconds")