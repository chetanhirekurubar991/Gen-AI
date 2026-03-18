from fastapi import FastAPI
from pydantic import BaseModel
import random, time

fake_cache = {}

import threading

semaphore = threading.Semaphore(10)


class ChatRequest(BaseModel):
    message: str


app = FastAPI()


@app.get("/health")
def healthcheck():
    return {"status": "OK"}


@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message
    if message in fake_cache:
        return {"response": fake_cache[message], "source": "cache"}

    acquired = semaphore.acquire(timeout=5)
    if not acquired:
        return {"Error": "service busy"}, 503
    try:
        time.sleep(random.uniform(0.5, 2))
        response_text = f"AI response to: {message}"
        fake_cache[message] = response_text
    finally:
        semaphore.release()
    return {"response": response_text, "source": "llm"}
