from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.schemas import DocumentOut
from app.services.document_service import process_document

router = APIRouter(prefix="/documents", tags=["Documentos"])

ALLOWED_EXTENSIONS = (".pdf", ".txt", ".md", ".csv")


@router.post(
    "/upload",
    response_model=DocumentOut,
    summary="Cargar documento",
    description="Sube un archivo (.pdf, .txt, .md, .csv), extrae el texto, genera embeddings y lo almacena.",
)
async def upload_document(
    file: UploadFile = File(..., description="Archivo a procesar"),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail=f"Solo se aceptan: {', '.join(ALLOWED_EXTENSIONS)}")
    try:
        return await process_document(file, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
