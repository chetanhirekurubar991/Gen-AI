from sqlmodel import Session,select
from fastapi import FastAPI,Depends
from pydantic import BaseModel
from database import create_db,get_db
from models import ChatMessage
import ollama
app=FastAPI()

@app.on_event("startup")
def on_startup():
    create_db()

class ChatRequest(BaseModel):
    session_id:str
    message:str
@app.post("/chat")
def chat(request:ChatRequest,db: Session=Depends(get_db)):
    user_msg=ChatMessage(
        session_id=request.session_id,
        role="user",
        content=request.message
    )
    db.add(user_msg)
    db.commit()

    statement=select(ChatMessage).where(ChatMessage.session_id==request.session_id).group_by(ChatMessage.crreated_at)
    history=db.exec(statement).all()

    messages=[
        {"role":"user","content":msg.content} for msg in history
    ]

    response=ollama.chat(
        model="deepseek-coder:6.7b",
        messages=messages
    )
    reply=response["message"]["content"]

    assistant_msg=ChatMessage(
        session_id=request.session_id,
        role="Assistant",
        content=reply
    )
    db.add(assistant_msg)
    db.commit()

    return {'reply':reply}

@app.get("/history/{session_id}")
def get_history(session_id:str,db: Session=Depends(get_db)):
    messages=db.exec(select(ChatMessage).where(ChatMessage.session_id==session_id).order_by(ChatMessage.created_at)).all()
    return {"messages": [{"role": m.role, "content": m.content} for m in messages]}