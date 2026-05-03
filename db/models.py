from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Note:
    id: Optional[int]
    contenido: str
    tag: str
    created_at: datetime
    updated_at: datetime
    pinecone_id: Optional[str] = None
    discord_message_id: Optional[str] = None
