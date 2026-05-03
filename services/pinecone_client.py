import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

class PineconeClient:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "engram-index")
        self._init_index()
        self.index = self.pc.Index(self.index_name)

    def _init_index(self):
        active_indexes = [idx.name for idx in self.pc.list_indexes()]
        if self.index_name not in active_indexes:
            print(f"Creando índice {self.index_name} para vectores de 768 dimensiones...")
            self.pc.create_index(
                name=self.index_name,
                dimension=768,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )

    def upsert_vector(self, nota_id, vector, metadata):
        self.index.upsert(
            vectors=[(str(nota_id), vector, metadata)]
        )

    def delete_vector(self, nota_id):
        self.index.delete(ids=[str(nota_id)])

    def query_similar(self, vector, top_k=5):
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return results
