from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import CHROMA_DIR



_embeddings = HuggingFaceEmbeddings()
_db = Chroma(persist_directory=CHROMA_DIR, embedding_function=_embeddings)


def retrieve(query):
    return _db.similarity_search(query, k=3)
