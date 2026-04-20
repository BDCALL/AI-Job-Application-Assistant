import os
os.environ["OPENAI_API_KEY"] = ""
from langchain_community.document_loaders import PyPDFLoader

user_cv = PyPDFLoader("data/cv.pdf")
job_description = PyPDFLoader("data/job.pdf")

cv_docs = user_cv.load()
job_docs = job_description.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)

cv_documents = splitter.split_documents(cv_docs)
job_documents = splitter.split_documents(job_docs)

for docs in cv_documents:
    docs.metadata["source"] = "CV"

for docs in job_documents:
    docs.metadata["source"] = "JOB"

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(cv_documents+job_documents, embeddings)
retriever = db.as_retriever(
    search_kwargs={"k": 6}
)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model= "gpt-4.1-mini", temperature=0)

from langchain_core.prompts import PromptTemplate
prompt = PromptTemplate(input_variables=["context","question"], 
                        template = """
You Are An AI career advisor,
You will receive:
- CV information
-Job Description Information

Your task is to compare them.

Instructions:
- Clearly seperate CV and Job Insights
- Be concise but informative

Return in this format:

Fit Score : <0-100>
<score>

Strenghts:
- ...

Missing Skills:
- ...

Suggestions:
- ...

Cover Letter:
<short tailored paragraph

Context:
{context}

Question:
{question}
""")

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm = llm, retriever = retriever, chain_type_kwargs = {"prompt" : prompt})

from langchain.tools import Tool

def calculator(x):
    return str(eval(x))

tools = [
    Tool(
        name = "Calculator",
        func = calculator,
        description = "Use this for math calculation"
    ),
    Tool(
        name = "Career Advisor",
        func = qa_chain.run,
        description = "Use this to give advise for cv and job questions"
    )
]

from langchain.agents import initialize_agent
agent = initialize_agent(tools = tools, llm=llm, agent="chat-conversational-react-description", memory = memory, verbose = True)

print("AI application Assistant Ready")

while True:
    query = input("\nAsk:")
    if query.lower() == "exit":
        break
    response = agent.invoke({"input":query})
    print("\nAnswer:", response["output"])