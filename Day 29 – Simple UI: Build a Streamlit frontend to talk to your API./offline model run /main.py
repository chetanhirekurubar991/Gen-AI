from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

MODEL_NAME = "deepseek-coder:6.7b"

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": request.message,
                "stream": False
            }
        )

        result = response.json()

        return {"response": result["response"]}

    except Exception as e:
        return {"error": str(e)}
