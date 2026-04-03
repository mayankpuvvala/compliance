from fastapi import FastAPI, UploadFile, File
import os
from pydantic import BaseModel

from app.rag import (
    process_new_document,
    ask_query,
    generate_summary,
    extract_compliance
)

app = FastAPI()

BASE_PATH = "data/sample_docs"

class QueryRequest(BaseModel):
    query: str
    filename: str


@app.get("/")
def home():
    return {"status": "running"}


# -------------------------
# UPLOAD
# -------------------------
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    path = os.path.join(BASE_PATH, file.filename)

    with open(path, "wb") as f:
        f.write(file.file.read())

    result = process_new_document(path)

    return {
        "filename": file.filename,
        "result": result
    }


# -------------------------
# ASK
# -------------------------
@app.post("/ask")
def ask(req: QueryRequest):
    path = os.path.join(BASE_PATH, req.filename)
    return ask_query(req.query, path)


@app.get("/summary")
def summary():
    return generate_summary()


@app.get("/compliance")
def compliance():
    return extract_compliance()