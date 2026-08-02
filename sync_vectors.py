import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from services.pinecone_client import PineconeClient
from services.gemini_client import GeminiClient
from db.connection import DBConnection
from core.notes import set_pinecone_id

async def main():
    print("🔄 Iniciando sincronización completa de vectores en Pinecone...")
    
    pool = await DBConnection.get_pool()
    query = "SELECT id, titulo, contenido, tag, created_at FROM notas ORDER BY id ASC;"
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(query)
        notes = [dict(r) for r in rows]
        
    print(f"📋 Encontradas {len(notes)} notas en PostgreSQL.")
    
    if not notes:
        print("⚠️ No hay notas en la base de datos para sincronizar.")
        await DBConnection.close()
        return

    gemini = GeminiClient()
    pinecone = PineconeClient()
    
    print("🗑️ Vaciando índice de Pinecone para eliminar vectores obsoletos/fantasmas...")
    try:
        pinecone.index.delete(delete_all=True)
        print("✅ Índice de Pinecone vaciado correctamente.")
    except Exception as e:
        print(f"❌ Error al vaciar Pinecone: {e}")
        print("Procediendo a subir las notas existentes de todos modos...")

    print("🧠 Generando embeddings e indexando notas en Pinecone...")
    success_count = 0
    for note in notes:
        nota_id = note['id']
        titulo = note['titulo']
        contenido = note['contenido']
        tag = note['tag']
        created_at = note['created_at']
        
        try:
            input_text = f"Título: {titulo}\n\nContenido: {contenido}"
            
            vector = await gemini.get_embedding(input_text, task_type='RETRIEVAL_DOCUMENT')
            
            metadata = {
                "nota_id": nota_id,
                "titulo": titulo,
                "tag": tag,
                "created_at": str(created_at) if created_at else str(datetime.now())
            }
            
            pinecone.upsert_vector(nota_id, vector, metadata)
            
            await set_pinecone_id(nota_id, str(nota_id))
            
            print(f"   🔹 Nota #{nota_id} sincronizada correctamente. (Título: '{titulo}')")
            success_count += 1
        except Exception as e:
            print(f"   ❌ Error al procesar Nota #{nota_id}: {e}")
            
    print(f"\n✨ Sincronización completada. Se indexaron {success_count} de {len(notes)} notas con éxito.")
    
    await DBConnection.close()

if __name__ == "__main__":
    asyncio.run(main())
