from langchain_community.document_loaders import PyPDFLoader

def load_data(path : str):
    loader = PyPDFLoader(path)
    return loader.load()