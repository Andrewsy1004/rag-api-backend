from datetime import datetime
from pydantic import BaseModel, Field


class DocumentOut(BaseModel):
    id: int
    filename: str
    created_at: datetime
    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, examples=["¿De qué trata el documento?"])


class ChatResponse(BaseModel):
    id: int
    question: str
    answer: str
    relevance_score: float = Field(description="Similitud coseno promedio (0-1). Más cerca de 1 = pregunta más coherente con los documentos.")
    created_at: datetime
    model_config = {"from_attributes": True}


class ChatHistoryItem(BaseModel):
    id: int
    question: str
    answer: str
    relevance_score: float
    fecha: str = Field(description="Fecha (YYYY-MM-DD)")
    hora: str = Field(description="Hora (HH:MM:SS)")
    model_config = {"from_attributes": True}
