from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.models.models import ChatMessage
from app.services.embedding_service import generate_embedding

_settings = get_settings()
_client = AsyncOpenAI(api_key=_settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """Eres un asistente que responde ÚNICAMENTE con la información del contexto proporcionado.

Reglas estrictas:
- Si el contexto contiene la respuesta, responde de forma clara y concisa.
- Si el contexto NO contiene la información, responde EXACTAMENTE: "Esa información no la conozco. Si tienes más preguntas, déjame saber."
- NUNCA inventes información que no esté en el contexto.
"""


MIN_SIMILARITY = 0.45
NO_INFO_RESPONSE = "Esa información no la conozco. Si tienes más preguntas, déjame saber."


async def _retrieve_context(q_embedding: list[float], db: AsyncSession, top_k: int = 5) -> tuple[str, float]:
    query = text(
        "SELECT text, 1 - (embedding <=> :emb) AS similarity "
        "FROM chunks ORDER BY embedding <=> :emb LIMIT :k"
    )
    result = await db.execute(query, {"emb": str(q_embedding), "k": top_k})
    rows = result.fetchall()

    relevant = [(row[0], row[1]) for row in rows if row[1] >= MIN_SIMILARITY]

    if not relevant:
        return "", 0.0

    context = "\n---\n".join(r[0] for r in relevant)
    avg_similarity = round(sum(r[1] for r in relevant) / len(relevant), 4)
    return context, avg_similarity


async def ask(question: str, db: AsyncSession) -> ChatMessage:
    q_embedding = await generate_embedding(question)
    context, relevance_score = await _retrieve_context(q_embedding, db)

    if not context:
        answer = NO_INFO_RESPONSE
    else:
        completion = await _client.chat.completions.create(
            model=_settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {question}"},
            ],
            temperature=0.2,
        )
        answer = completion.choices[0].message.content

    msg = ChatMessage(question=question, answer=answer, relevance_score=relevance_score)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg
