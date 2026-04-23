from rag.chain import build_chain
from rag.loader import load_data
from rag.splitter import split_docs
from rag.vectorstore import create_db
from core.prompt import get_prompt
import re

def extract_skills(text):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return set(words)

def compute_score(cv_docs, job_docs):
    cv_text = " ".join([doc.page_content for doc in cv_docs])
    job_text = " ".join([doc.page_content for doc in job_docs])

    cv_skills = extract_skills(cv_text)
    job_skills = extract_skills(job_text)

    if len(job_skills) == 0:
        return 0

    match = len(cv_skills.intersection(job_skills))
    score = int((match / len(job_skills)) * 100)

    return score

def build_pipeline (cv_path, job_path):
    cv_docs = load_data(cv_path)
    job_docs = load_data(job_path)

    score  = compute_score(cv_docs, job_docs)
    cv_chunks = split_docs(cv_docs)
    job_chunks = split_docs(job_docs)

    for chunk in cv_chunks:
        chunk.metadata["source"] = "CV"
    for chunk in job_chunks:
        chunk.metadata["source"] = "JOB"

    db = create_db(cv_chunks + job_chunks)

    prompt = get_prompt()

    return build_chain(db,prompt), score
