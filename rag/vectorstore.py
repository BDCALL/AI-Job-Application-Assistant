from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def create_db(chunks):
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks,embeddings)
    return db