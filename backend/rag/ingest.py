from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

BASE_DIR =  os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "kb_data", "terraform_docs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

def ingest():
    loader = DirectoryLoader(DATA_DIR)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings()
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_DIR)

if __name__ == "__main__":
    ingest()