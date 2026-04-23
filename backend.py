from fastapi import FastAPI
from pydantic import BaseModel
from api import build_pipeline
from langchain_openai import ChatOpenAI
import os

app = FastAPI()

qa_chain = None
score = None

class Query(BaseModel):
    question: str

# Check API key
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY not set")

llm_general = ChatOpenAI(model="gpt-4.1-mini", temperature=0.7)

def is_career_question(question: str) -> bool:
    keywords = [
        "cv", "resume", "job", "career", "skills",
        "experience", "fit", "apply", "application",
        "cover letter", "interview"
    ]

    q = question.lower()

    if any(word in q for word in keywords):
        return True

    if len(q.split()) > 3:
        decision = llm_general.invoke(
            f"Is this about jobs, CVs, or career advice? YES or NO: {question}"
        ).content.upper()

        return "YES" in decision

    return False

@app.post("/setup")
def setup():
    global qa_chain, score

    qa_chain, score = build_pipeline("data/temp_cv.pdf", "data/temp_job.pdf")

    return {"status": "ready", "score": score}

@app.post("/ask")
def ask(q: Query):
    if qa_chain is None:
        return {"error": "Run /setup first"}

    try:
        career_mode = is_career_question(q.question)

        if career_mode:
            response = qa_chain.invoke({"query": q.question})["result"]
            mode = "career"
        else:
            response = llm_general.invoke(q.question).content
            mode = "chat"

        return {"answer": response, "mode": mode}

    except Exception as e:
        return {"error": str(e)}