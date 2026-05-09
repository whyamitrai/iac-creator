import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "kb_data", "terraform_docs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

load_dotenv(os.path.join(BASE_DIR, ".env"))

region = os.getenv("AWS_REGION")
model = os.getenv("OLLAMA_MODEL")
