from db.connection import DBConnection

async def create_note(titulo, contenido, tag, discord_message_id):
    pool = await DBConnection.get_pool()
    
    check_query = "SELECT id FROM notas WHERE contenido = $1 AND titulo = $2 LIMIT 1;"
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(check_query, contenido, titulo)
        if existing:
            return {"error": "duplicate", "id": existing['id']}
            
        query = """
            INSERT INTO notas (titulo, contenido, tag, discord_message_id)
            VALUES ($1, $2, $3, $4)
            RETURNING id, created_at;
        """
        row = await conn.fetchrow(query, titulo, contenido, tag, discord_message_id)
        return dict(row)

async def get_pending_notes():
    pool = await DBConnection.get_pool()
    query = """
        SELECT id, titulo, contenido, tag, created_at 
        FROM notas 
        WHERE pinecone_id IS NULL 
        ORDER BY created_at ASC;
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(r) for r in rows]

async def update_note(nota_id, titulo, contenido):
    pool = await DBConnection.get_pool()
    query = """
        UPDATE notas 
        SET titulo = $1, contenido = $2, updated_at = NOW()
        WHERE id = $3
        RETURNING id;
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, titulo, contenido, nota_id)
        return dict(row) if row else None

async def delete_note(nota_id):
    pool = await DBConnection.get_pool()
    query = "DELETE FROM notas WHERE id = $1 RETURNING pinecone_id;"
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, nota_id)
        return dict(row) if row else None

async def set_pinecone_id(nota_id, pinecone_id):
    pool = await DBConnection.get_pool()
    query = "UPDATE notas SET pinecone_id = $1 WHERE id = $2;"
    async with pool.acquire() as conn:
        await conn.execute(query, pinecone_id, nota_id)
