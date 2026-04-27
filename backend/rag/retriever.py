from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import CHROMA_DIR

def retrieve(query):
    embeddings = HuggingFaceEmbeddings()
    db = Chroma(persist_directory = CHROMA_DIR, embedding_function = embeddings)
    result = db.similarity_search(query, k = 3)
    return result