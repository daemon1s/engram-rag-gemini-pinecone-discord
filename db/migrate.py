import asyncio
import os
from db.connection import DBConnection

async def run_migrations():
    print("Iniciando migraciones...")
    migrations_dir = 'db/migrations'
    
    files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
    
    for file_name in files:
        file_path = os.path.join(migrations_dir, file_name)
        print(f"Ejecutando {file_name}...")
        await DBConnection.execute_migration(file_path)
    
    await DBConnection.close()
    print("Migraciones completadas con éxito.")

if __name__ == "__main__":
    asyncio.run(run_migrations())
