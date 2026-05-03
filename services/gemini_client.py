import os
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.text_model = 'gemini-3.1-flash-lite-preview'
        self.embedding_model = 'gemini-embedding-2'
        self.max_retries = 6
        self.base_delay = 3

    async def _retry_call(self, func, *args, **kwargs):
        for i in range(self.max_retries):
            try:
                return await asyncio.to_thread(func, *args, **kwargs)
            except Exception as e:
                if i == self.max_retries - 1:
                    raise e
                
                delay = self.base_delay * (2 ** i)
                print(f"❌ Error en Gemini: {str(e)}")
                print(f"Gemini API Retry {i+1}/{self.max_retries}: {delay}s wait")
                await asyncio.sleep(delay)

    async def get_embedding(self, text):
        def call():
            result = self.client.models.embed_content(
                model=self.embedding_model,
                contents=text,
                config={
                    'task_type': 'RETRIEVAL_DOCUMENT',
                    'output_dimensionality': 768
                }
            )
            return result.embeddings[0].values
        
        return await self._retry_call(call)

    async def get_response(self, prompt, context=""):
        full_prompt = f"Contexto:\n{context}\n\nPregunta: {prompt}"
        
        def call():
            response = self.client.models.generate_content(
                model=self.text_model,
                contents=full_prompt
            )
            return response.text

        return await self._retry_call(call)
