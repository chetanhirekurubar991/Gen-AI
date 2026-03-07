from sqlmodel import SQLModel,Field
from datetime import datetime
from typing import Optional

class ChatMessage(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    session_id:int
    role:str
    content:str
    created_at:datetime=Field(default_factory=datetime.utcnow)