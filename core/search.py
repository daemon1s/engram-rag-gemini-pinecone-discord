from services.gemini_client import GeminiClient
from services.pinecone_client import PineconeClient

gemini = GeminiClient()
pinecone = PineconeClient()

import asyncio

async def get_context(query, top_k=5):
    vector = await gemini.get_embedding(query)
    
    # Pinecone es síncrono, lo corremos en un thread para no bloquear
    results = await asyncio.to_thread(pinecone.query_similar, vector, top_k=top_k)
    return results
