from datetime import datetime
from services.gemini_client import GeminiClient
from services.pinecone_client import PineconeClient
from core.notes import set_pinecone_id

gemini = GeminiClient()
pinecone = PineconeClient()

async def process_and_upload_note(nota_id, titulo, contenido, tag, created_at=None):
    input_text = f"Título: {titulo}\n\nContenido: {contenido}"
    vector = await gemini.get_embedding(input_text)
    
    metadata = {
        "nota_id": nota_id,
        "titulo": titulo,
        "tag": tag,
        "created_at": str(created_at) if created_at else str(datetime.now())
    }
    
    pinecone.upsert_vector(nota_id, vector, metadata)
    
    await set_pinecone_id(nota_id, str(nota_id))
    
    print(f"Nota {nota_id} embeddeada y subida a Pinecone con éxito.")
