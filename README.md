# 🧠 AI-Powered Compliance Risk Analyzer (RAG + LLM)

An end-to-end **Retrieval-Augmented Generation (RAG)** system that ingests regulatory documents (PDF/TXT), analyzes them using LLMs, and extracts **compliance risks, obligations, and conflicts across multiple documents**.

---

## 🚀 Features

### 📄 Document Ingestion
- Supports **PDF and TXT files**
- Automatically splits documents into chunks
- Stores embeddings in **Chroma Vector DB**

### 🔍 Intelligent Retrieval (RAG)
- Retrieves **context-aware chunks** based on user queries
- Uses semantic search with embeddings

### 🤖 LLM-Powered Analysis
- Generates:
  - Summary
  - Obligations
  - Rules

### ⚖️ Multi-Document Comparison
When multiple documents are uploaded:
- Detects:
  - Similarities
  - Differences
  - Conflicts
  - New rules introduced

### ⚠️ Compliance Risk Extraction
- Identifies risks across documents
- Classifies into:
  - Low
  - Medium
  - High

### 💬 Query System
- Ask questions grounded in uploaded documents
- Strict context-based answering (no hallucination outside scope)

---

## ⚙️ Tech Stack

- **Backend:** FastAPI
- **LLM:** Azure OpenAI (via custom endpoint)
- **Embeddings:** text-embedding-3-large
- **Vector DB:** ChromaDB
- **Framework:** LangChain
- **Parsing:** PyPDFLoader

---

