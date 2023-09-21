'''
1. getting all the details of the user's complaint
2. using that complaint to map to the best suitable government employee
    a. initial complaint -> llm routing -> trying to get the best fitted \
    employees list -> vector database + langchain query
    b. giving the user this freedom to select any one of the filtered employees \
    or we may  even automate this as using  Map re-rank concept available in langchain docs\
    or any other better way
3. then re-processing the complaint and connecting it with the employee
'''

import os
import getpass

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import TextLoader


loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

MONGODB_ATLAS_CLUSTER_URI = getpass.getpass("mongodb+srv://codyaanSIH:VEkE6wjohQ9v01De@cluster0.vkfifhe.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
os.environ["OPENAI_API_KEY"] = getpass.getpass("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")

from pymongo import MongoClient

# initialize MongoDB python client
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

db_name = "test"
collection_name = "test"
collection = client[db_name][collection_name]
index_name = "default"

# insert the documents in MongoDB Atlas with their embedding
docsearch = MongoDBAtlasVectorSearch.from_documents(
    docs, embeddings, collection=collection, index_name=index_name
)

# perform a similarity search between the embedding of the query and the embeddings of the documents
query = "test1"
docs = docsearch.similarity_search(query)