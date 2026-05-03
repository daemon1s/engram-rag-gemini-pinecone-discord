import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

class DBConnection:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                os.getenv("POSTGRES_URL"),
                min_size=1,
                max_size=10
            )
        return cls._pool

    @classmethod
    async def execute_migration(cls, file_path):
        pool = await cls.get_pool()
        with open(file_path, 'r') as f:
            sql = f.read()
        
        async with pool.acquire() as conn:
            await conn.execute(sql)
            print(f"Migración {file_path} ejecutada correctamente.")

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
