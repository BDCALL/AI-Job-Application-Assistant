from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def build_chain(db,prompt):
    llm = ChatOpenAI(model = "gpt-4.1-mini", temperature=0)
    retriever = db.as_retriever(search_kwargs= {"k" : 6}, search_type = "mmr")
    qa_chain = RetrievalQA.from_chain_type(llm = llm, retriever = retriever, chain_type_kwargs = {"prompt" : prompt})
    return qa_chain