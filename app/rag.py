import os
import json

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.config import get_llm
from app.embeddings import CustomEmbeddings
from app.knowledge_store import load_store, add_document_entry


DB_PATH = "db"


# -------------------------
# SAFE JSON PARSER
# -------------------------
def safe_json_parse(text):
    try:
        text = text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except Exception:
        return {"error": "Invalid JSON", "raw": text}


# -------------------------
# LOAD + SPLIT
# -------------------------
def load_and_split(file_path):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            docs = [Document(page_content=f.read())]
    else:
        raise ValueError("Unsupported file")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(docs)


# -------------------------
# INGEST INTO VECTOR DB
# -------------------------
def ingest_to_vector_db(chunks, file_name):
    vectordb = Chroma(
        persist_directory=DB_PATH,
        embedding_function=CustomEmbeddings()
    )

    # add metadata (VERY IMPORTANT)
    for c in chunks:
        c.metadata["source"] = file_name

    vectordb.add_documents(chunks)


# -------------------------
# RETRIEVE RELEVANT CONTEXT
# -------------------------
def retrieve_context(query, file_name, k=5):
    vectordb = Chroma(
        persist_directory=DB_PATH,
        embedding_function=CustomEmbeddings()
    )

    docs = vectordb.similarity_search(query, k=k)

    # optional: filter by file
    docs = [d for d in docs if d.metadata.get("source") == file_name]

    return "\n\n".join([d.page_content for d in docs])


# -------------------------
# PROCESS DOCUMENT
# -------------------------
def process_new_document(file_path):
    file_name = os.path.basename(file_path)

    chunks = load_and_split(file_path)

    # ✅ STORE in vector DB
    ingest_to_vector_db(chunks, file_name)

    # still use limited context for summary
    context = "\n\n".join([c.page_content for c in chunks[:15]])

    llm = get_llm()

    prompt = f"""
AI-Powered Regulatory Compliance Assistant for Capital Markets

Context:
{context}

Return JSON:
{{
 "summary": "...",
 "obligations": ["..."],
 "rules": ["..."]
}}
"""

    analysis = safe_json_parse(llm.invoke(prompt).content)

    # -------------------------
    # COMPARISON
    # -------------------------
    existing = load_store()

    prompt = f"""
Compare:

NEW: {json.dumps(analysis)}
EXISTING: {json.dumps(existing)}

Return JSON:
{{
 "similarities": [],
 "differences": [],
 "conflicts": [],
 "new_rules": []
}}
"""

    comparison = safe_json_parse(llm.invoke(prompt).content)

    # -------------------------
    # STORE
    # -------------------------
    entry = {
        "document": file_name,
        "summary": analysis.get("summary"),
        "rules": analysis.get("rules", [])
    }

    add_document_entry(entry)

    return {
        "analysis": analysis,
        "comparison": comparison
    }


# -------------------------
# ASK QUESTION (REAL RAG 🔥)
# -------------------------
def ask_query(query, file_path):
    file_name = os.path.basename(file_path)

    # ✅ retrieve relevant chunks
    context = retrieve_context(query, file_name, k=5)

    llm = get_llm()

    prompt = f"""

You are a compliance assistant and if someone asks any other question which is completely irrelevant say it is out of your scope
Answer using the context below.
If partially available, still answer.

Context:
{context}

Question:
{query}

Return JSON:
{{
 "answer": "...",
 "key_points": []
}}
"""

    return safe_json_parse(llm.invoke(prompt).content)


# -------------------------
# GLOBAL SUMMARY
# -------------------------
def generate_summary():
    store = load_store()
    llm = get_llm()

    prompt = f"""
You are a compliance assistant and if someone asks any other question which is completely irrelevant say it is out of your scope
Summarize all documents:

{json.dumps(store)}

Return JSON:
{{ "summary": "..." }}
"""

    return safe_json_parse(llm.invoke(prompt).content)


# -------------------------
# COMPLIANCE EXTRACTION
# -------------------------
def extract_compliance():
    store = load_store()
    llm = get_llm()

    prompt = f"""
You are a compliance assistant and if someone asks any other question which is completely irrelevant say it is out of your scope
Extract compliance risks:

{json.dumps(store)}

Return JSON:
{{
 "compliances": [
  {{
   "title": "...",
   "description": "...",
   "risk_level": "Low/Medium/High"
  }}
 ]
}}
"""

    return safe_json_parse(llm.invoke(prompt).content)