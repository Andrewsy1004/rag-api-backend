from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import ChatMessage
from app.schemas.schemas import ChatRequest, ChatResponse, ChatHistoryItem
from app.services.chat_service import ask

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/ask",
    response_model=ChatResponse,
    summary="Hacer una pregunta",
    description="Envía una pregunta al sistema RAG. Busca contexto en los documentos y genera una respuesta.",
)
async def ask_question(
    body: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ask(body.question, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/history",
    response_model=list[ChatHistoryItem],
    summary="Historial de chat",
    description="Retorna las conversaciones guardadas con fecha y hora.",
)
async def get_history(
    limit: int = Query(50, ge=1, le=500, description="Cantidad máxima de mensajes"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatMessage).order_by(ChatMessage.created_at.desc()).limit(limit)
    )
    return [
        ChatHistoryItem(
            id=m.id,
            question=m.question,
            answer=m.answer,
            relevance_score=m.relevance_score,
            fecha=m.created_at.strftime("%Y-%m-%d"),
            hora=m.created_at.strftime("%H:%M:%S"),
        )
        for m in result.scalars().all()
    ]
