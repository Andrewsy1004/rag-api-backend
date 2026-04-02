from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import text


from app.core.database import engine, Base
from app.routers import documents, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="RAG API",
    description=(
        "API de Retrieval-Augmented Generation.\n\n"
        "- **Carga documentos PDF/TXT** y los almacena como embeddings en PostgreSQL + pgvector.\n"
        "- **Haz preguntas** y obtén respuestas basadas en tus documentos.\n"
        "- **Consulta el historial** de preguntas y respuestas con fecha y hora."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")


@app.get("/health", tags=["Health"], summary="Estado del servicio")
async def health():
    return {"status": "ok"}
