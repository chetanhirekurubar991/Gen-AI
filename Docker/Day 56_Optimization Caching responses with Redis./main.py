import hashlib
import logging
import redis
from fastapi import FastAPI
from config import settings

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

app=FastAPI(docs_url="/chetan")

redis_client=redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    # if hosting on azure needs these 3 security layers i wrote half and comment that in below make it full before hosting
    # password=settings.redis_password,
    # ssl=True,
    decode_responses=True,
)

@app.on_event("startup")
def startup_event():
    try:
        redis_client.ping()
        logger.info("Redis connected Successfully")
    except redis.ConnectionError as e:
        logger.error(f"Redis connection Failed")

def get_cache_key(question : str)->str:
    hash=hashlib.md5(question.encode()).hexdigest()
    return f"chat:{hash}"

@app.get('/')
def root():
    return {'app_name':settings.app_name}

@app.get("/chat")
def chat(question:str):
    cache_key=get_cache_key(question)
    cached=redis_client.get(cache_key)
    if cached:
        logger.info(f"Cache HIT for key : {cache_key}")
        return {"source":"cache","answer":cached}
    logger.info(f"Cache MISS for key: {cache_key}")
    llm_answer=f"This is simulated answer to:'{question}'"
    redis_client.setex(cache_key,3600,llm_answer)
    logger.info(f"Cached answer for key: {cache_key}")
    return {"source":"llm","answer":llm_answer}