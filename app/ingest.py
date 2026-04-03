import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from openai import OpenAI
import httpx

# ✅ FIXED absolute paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "sample_docs")
DB_PATH = os.path.join(BASE_DIR, "db")

load_dotenv()
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ shared HTTP client (SSL bypass)
http_client = httpx.Client(verify=False)

# ✅ OpenAI client
openai_client = OpenAI(
    base_url="https://genailab.tcs.in",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    http_client=http_client
)

# ✅ CUSTOM EMBEDDING CLASS
class CustomEmbeddings:
    def embed_documents(self, texts):
        response = openai_client.embeddings.create(
            model="azure/genailab-maas-text-embedding-3-large",
            input=texts
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text):
        response = openai_client.embeddings.create(
            model="azure/genailab-maas-text-embedding-3-large",
            input=[text]
        )
        return response.data[0].embedding

from langchain_core.documents import Document

def load_documents():
    documents = []

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ DATA_PATH not found: {DATA_PATH}")

    files = os.listdir(DATA_PATH)

    if not files:
        raise ValueError(f"⚠️ No files found in: {DATA_PATH}")

    for file in files:
        file_path = os.path.join(DATA_PATH, file)
        print(f"📄 Loading: {file_path}")

        # -------------------------
        # ✅ PDF FILES
        # -------------------------
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            for d in docs:
                d.metadata["source"] = file  # ✅ IMPORTANT

            documents.extend(docs)

        # -------------------------
        # ✅ TXT FILES
        # -------------------------
        elif file.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": file}
                )
            )

        # -------------------------
        # ❌ SKIP OTHER FILES
        # -------------------------
        else:
            print(f"⚠️ Skipping unsupported file: {file}")

    return documents

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)


def main():
    print("📄 Loading documents...")
    docs = load_documents()

    print(f"✅ Loaded {len(docs)} pages")

    print("✂️ Splitting documents...")
    chunks = split_docs(docs)

    print(f"✅ Created {len(chunks)} chunks")

    print("🧠 Generating embeddings & storing in Chroma...")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=CustomEmbeddings(),  # ✅ FIXED
        persist_directory=DB_PATH
    )

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    main()