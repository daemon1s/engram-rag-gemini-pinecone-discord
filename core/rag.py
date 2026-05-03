from core.search import get_context
from services.gemini_client import GeminiClient
from db.connection import DBConnection

gemini = GeminiClient()

async def answer_with_rag(query):
    search_results = await get_context(query)
    nota_ids = [int(match.id) for match in search_results.matches]
    
    if not nota_ids:
        return "No encontré notas relacionadas con tu pregunta."

    pool = await DBConnection.get_pool()
    query_db = "SELECT contenido, tag FROM notas WHERE id = ANY($1::int[])"
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(query_db, nota_ids)
        
    context_parts = []
    for row in rows:
        context_parts.append(f"[{row['tag']}]: {row['contenido']}")
    
    context_text = "\n---\n".join(context_parts)
    
    response = await gemini.get_response(query, context=context_text)
    return response
