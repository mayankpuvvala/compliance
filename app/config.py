import os
from dotenv import load_dotenv
import httpx
from openai import OpenAI
from langchain_openai import ChatOpenAI

load_dotenv()

BASE_URL = "https://genailab.tcs.in"
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

http_client = httpx.Client(verify=False)

# -------------------------
# OPENAI CLIENT
# -------------------------
openai_client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    http_client=http_client
)

# -------------------------
# LLM
# -------------------------
def get_llm():
    return ChatOpenAI(
        base_url=BASE_URL,
        model="azure/genailab-maas-gpt-4.1",
        api_key=API_KEY,
        http_client=http_client,
        temperature=0.2
    )