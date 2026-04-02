# 🩺 MaterniAI — RAG-based Obstetric Assistant API

An AI powered obstetric assistant that provides clinical guidance on maternal health using local evidence from the Colombian context. Built with Retrieval-Augmented Generation (RAG), it retrieves relevant information from uploaded clinical documents and generates grounded answers using OpenAI, reducing hallucinations and ensuring responses are backed by verifiable sources.

> ⚠️ This tool does not replace medical professionals. It serves as an additional support resource based on clinical guidelines and scientific evidence.

## 🛠️ Tech Stack

- ⚡ **FastAPI**  Async REST API with Swagger documentation
- 🗄️ **PostgreSQL + pgvector**  Vector database for semantic search
- 🧠 **OpenAI**  Embeddings (`text-embedding-3-small`) and completions (`gpt-4o-mini`)
- 🐳 **Docker**  Containerized deployment

## 📂 Project Structure

```
rag-project/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
└── app/
    ├── main.py
    ├── core/
    │   ├── config.py
    │   └── database.py
    ├── models/
    │   └── models.py
    ├── schemas/
    │   └── schemas.py
    ├── services/
    │   ├── embedding_service.py
    │   ├── document_service.py
    │   └── chat_service.py
    └── routers/
        ├── documents.py
        └── chat.py
```

## 🚀 Getting Started

1. Change the file `.env.example` to `.env` and set your OpenAI API key.
2. Run the Docker container with `docker-compose up -d --build`
3. Access the API at `http://localhost:8000/docs`

## 📡 Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/v1/documents/upload` | Upload a document (.pdf, .txt, .md, .csv) |
| POST | `/api/v1/chat/ask` | Ask a question to the RAG system |
| GET | `/api/v1/chat/history` | Chat history with date, time and relevance score |
| GET | `/health` | Health check |

## 📊 Relevance Score

Each response includes a `relevance_score` (0–1) indicating how closely the question matched the stored documents. Only chunks above the minimum similarity threshold are used to generate the answer.

| Score | Interpretation |
|-------|----------------|
| 🟢 0.85 – 1.0 | Highly relevant |
| 🟡 0.70 – 0.85 | Moderate |
| 🔴 < 0.70 | Low relevance |