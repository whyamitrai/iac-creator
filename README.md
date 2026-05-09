# IaC Creator

AI-powered Infrastructure as Code generator that uses RAG (Retrieval-Augmented Generation) and Terraform best practices to generate production-ready Terraform configurations from natural language descriptions.

## Architecture

```
User (Streamlit UI)
        │
        ▼
  FastAPI Backend
        │
        ▼
  LangGraph Agent ──────► ChromaDB (RAG)
        │                 (Terraform best practices)
        ▼
   Ollama (llama3.2)
        │
        ▼
  Terraform Code Output
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend API | FastAPI + Uvicorn |
| Agent Framework | LangGraph |
| LLM | Ollama (llama3.2) — swappable to AWS Bedrock |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| RAG Documents | Terraform best practices & naming conventions |

## Features

- Natural language to Terraform code generation
- RAG-powered — retrieves best practices before generating code
- Conversational agent built with LangGraph
- Local-first — runs entirely on your machine (no API keys needed)
- Modular architecture — easily swap LLM provider (Ollama ↔ Bedrock)
- Clean separation of frontend and backend

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed with `llama3.2` model pulled
- Git

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/iac-creator.git
   cd iac-creator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Pull Ollama model**
   ```bash
   ollama pull llama3.2
   ```

6. **Ingest RAG documents**
   ```bash
   python -m backend.rag.ingest
   ```

7. **Start the backend**
   ```bash
   uvicorn backend.main:app --reload
   ```

8. **Start the frontend** (new terminal)
   ```bash
   streamlit run frontend/app.py
   ```

## Usage

1. Open the Streamlit UI at `http://localhost:8501`
2. Describe your infrastructure need in natural language
3. The agent retrieves Terraform best practices via RAG
4. Generated Terraform code is displayed in the browser

**Example prompt:**
> Create an S3 bucket with versioning enabled and server-side encryption

## Project Structure

```
iac-creator/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment variables loader
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── agent/
│   │   └── graph.py         # LangGraph agent (RAG + generation)
│   └── rag/
│       ├── ingest.py        # Documents → ChromaDB
│       └── retriever.py     # ChromaDB similarity search
├── frontend/
│   └── app.py               # Streamlit UI
├── kb_data/
│   └── terraform_docs/      # RAG source documents
├── requirements.txt
├── .env.example
└── README.md
```

## Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

Services:
- **App** — `http://localhost:8501` (Streamlit) + `http://localhost:8000` (API)
- **Ollama** — `http://localhost:11434`

> Note: First run will pull the Ollama image and model (may take a few minutes).

## CI/CD

GitHub Actions pipeline runs on every push/PR to `main`:
- Python dependency installation
- Linting with flake8
- Docker image build verification

## Roadmap

- [x] Docker containerization
- [x] CI/CD pipeline
- [ ] Swap to AWS Bedrock (Claude) for production LLM
- [ ] Multi-turn conversation support
- [ ] Terraform plan validation
- [ ] More RAG documents (modules, security best practices)
