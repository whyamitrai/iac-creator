from dotenv import load_dotenv
import os 

load_dotenv()

region = os.getenv("AWS_REGION")
model = os.getenv("BEDROCK_MODEL")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "kb_data", "terraform_docs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")