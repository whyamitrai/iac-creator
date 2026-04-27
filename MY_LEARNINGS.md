# My Learnings — IaC Creator Project

> Doubts jo session mein aaye aur clear hue. Revision ke liye.

---

## Session 1 — Apr 27, 2026

### 1. FastAPI kyun use karte hain?

- **Separation of concerns** — Frontend (Streamlit) alag, backend (FastAPI) alag
- **Multiple clients** — Ek API likho, koi bhi frontend use kare (Streamlit, React, mobile app)
- **Production-ready** — Real companies mein frontend aur backend alag deploy hote hain
- **Interview mein** — "Decoupled architecture" bolna > "sab ek file mein daal diya"
- **Ek line mein:** FastAPI backend ka gate hai — bahar se koi bhi aaye, sab ek hi gate se andar aate hain

### 2. `__init__.py` kyun chahiye?

- Python ko batata hai ki ye folder ek "package" hai
- Bina iske `from backend.config import ...` fail hoga
- Khali file rakh do — bas Python ko signal chahiye

### 3. `.env` vs `.env.example`

- `.env` — actual secrets (gitignored, push nahi hoti)
- `.env.example` — template (push hoti hai, taaki dusre log samjhein kya set karna hai)
- Format: `KEY=value` (simple, no JSON, no curly braces)

### 4. `python-dotenv` kya karta hai?

- `.env` file se environment variables load karta hai
- `load_dotenv()` call karo → `.env` ki values `os.getenv()` se accessible ho jaati hain
- Bina iske manually environment variables set karne padte

### 5. `__file__` kya hai?

- Python ka built-in variable — har file mein automatically set hota hai
- Value = us file ka full path
- Example: `backend/rag/ingest.py` mein `__file__` = `D:\Learning\iac-creator\backend\rag\ingest.py`
- Tu pass nahi karta, Python khud set karta hai

### 6. `os.path.dirname()` kya karta hai?

- Path mein se last part hata deta hai — ek folder upar le jaata hai
- Example chain:
  ```
  os.path.dirname(".../backend/rag/ingest.py") → ".../backend/rag"
  os.path.dirname(".../backend/rag")           → ".../backend"
  os.path.dirname(".../backend")               → ".../" (project root)
  ```
- 3 baar call = 3 level upar (kyunki ingest.py project root se 3 level andar hai)

### 7. `os.path.join()` kya karta hai?

- Path ke parts ko OS-specific separator se jodta hai
- Example:
  ```python
  os.path.join("iac-creator", "kb_data", "terraform_docs")
  # Windows: "iac-creator\kb_data\terraform_docs"
  # Linux:   "iac-creator/kb_data/terraform_docs"
  ```
- Manually path likhega toh OS change hone pe toot sakta hai
- `os.path.join` har OS pe sahi kaam karta hai

### 8. Relative path vs Absolute path (via `__file__`)

- **Relative (`"../data/"`):** Terminal mein KAHAN khade ho uspe depend karta hai. Galat folder se run karo toh fail.
- **Absolute (`__file__` se calculate):** File ki location se calculate hota hai. Kahin se bhi run karo, sahi path milega.
- Rule: Scripts mein jo file access karte hain, hamesha `__file__` se path banao.

### 9. `if __name__ == "__main__"` kyun?

- Ye code sirf tab chalega jab tu directly `python ingest.py` run kare
- Agar koi dusri file `from ingest import ingest` kare toh automatically nahi chalega
- Standard practice — har script mein hona chahiye

### 10. RAG Ingest Flow

```
DirectoryLoader("path") → .load() → docs (list of documents)
    ↓
RecursiveCharacterTextSplitter(chunk_size, chunk_overlap) → .split_documents(docs) → chunks
    ↓
HuggingFaceEmbeddings() → embedding model object (ye sirf model hai, data nahi leta)
    ↓
Chroma.from_documents(documents=chunks, embedding=model, persist_directory="path")
    → internally har chunk ki embedding banata hai aur store karta hai
```

- **Chunk overlap:** Har chunk mein pichle chunk ke kuch characters overlap — taaki context break na ho
- **RecursiveCharacterTextSplitter:** Pehle paragraphs pe todta hai, phir sentences, phir words — jab tak chunk size fit na ho
- **HuggingFaceEmbeddings:** Pre-trained model (all-MiniLM-L6-v2), local chalega, free hai
- **Chroma.from_documents:** Ek call mein sab karta hai — embedding + store

### 11. GCC kya hai?

- **Global Capability Center** — jab foreign company (Google, JPMorgan, Walmart) India mein apna engineering office khole
- India mein 1800+ GCCs, 15L+ employees
- Ye directly hire karte hain (TCS/Infosys ke through nahi)
- 58% GCCs agentic AI mein invest kar rahe hain — tera LangGraph experience yahan valuable hai
