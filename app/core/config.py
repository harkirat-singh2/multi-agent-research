from langchain_nvidia_ai_endpoints import ChatNVIDIA
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatNVIDIA(
    model="meta/llama-3.1-8b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0.2,
    max_tokens=500
)