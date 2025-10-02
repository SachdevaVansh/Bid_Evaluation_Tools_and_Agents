from langchain_community.vectorstores import FAISS 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings 
from typing import List 
import streamlit as st 

## Euri Embeddings 
# euri_api_key=st.secrets["EURI_API_KEY"]
# import requests
# import numpy as np

# def generate_embeddings(text):
#     url = "https://api.euron.one/api/v1/euri/embeddings"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {euri_api_key}"
#     }
#     payload = {
#         "input": text,
#         "model": "text-embedding-3-small"
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     data = response.json()
    
#     embedding = np.array(data['data'][0]['embedding'])
    
#     return embedding

# class EuriEmbeddings(Embeddings):
#     def embed_documents(self,texts):
#         return [generate_embeddings(t).tolist() for t in texts]
    
#     def embed_query(self,text):
#         return generate_embeddings(text).tolist()

# # Create the object of the EuriEmbeddings class
# embeddings_euri = EuriEmbeddings()

def create_faiss_index(documents):
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    #embeddings=embeddings_euri 
    return FAISS.from_documents(documents, embeddings)

def retrieve_relevant_docs(vectorstore: FAISS, query:str, k:int=4):
    return vectorstore.similarity_search(query, k=k)