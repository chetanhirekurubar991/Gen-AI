"""Before running this code need the day56 all files except main.py
Because i just refactor: improve readability, type safety and error handling"
basic needed day 56 files are config.py and .env (but .env is optional because i set defaults values in config.py file)
"""

import hashlib
import logging
import redis
from fastapi import FastAPI
from config import settings

# --- Constants ---
CACHE_TTL_SECONDS = 3600

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(docs_url="/chetan")

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    # if hosting on azure needs these 3 security layers i wrote half and comment that in below make it full before hosting
    # password=settings.redis_password,
    # ssl=True,
    decode_responses=True,
)


@app.on_event("startup")
def startup_event() -> None:
    """
    Verify Redis connectivity on app startup.
    Fails loudly so misconfiguration is caught before serving traffic.
    """
    try:
        redis_client.ping()
        logger.info("Redis connected Successfully")
    except redis.ConnectionError as e:
        logger.error(f"Redis connection Failed: {e}")
        raise RuntimeError("Redis unavailable. Aborting startup.") from e


def get_cache_key(question: str) -> str:
    """
    Generate a deterministic Redis key from the question.
    MD5 keeps keys short and uniform regardless of question length.
    """
    hash_value = hashlib.md5(question.encode()).hexdigest()
    return f"chat:{hash_value}"


def get_cached_response(cache_key: str) -> str | None:
    """
    Fetch a cached LLM response from Redis.
    Returns None on cache miss so callers can branch cleanly.
    """
    return redis_client.get(cache_key)


def store_cached_response(cache_key: str, answer: str) -> None:
    """
    Persist LLM response in Redis to avoid redundant API calls
    for identical questions within the TTL window.
    """
    redis_client.setex(cache_key, CACHE_TTL_SECONDS, answer)


def call_llm(question: str) -> str:
    """
    Call the LLM and return its answer.
    Isolated here so swapping models or providers touches one function only.
    """
    return f"This is a simulated answer to: '{question}'"


@app.get("/")
def root():
    """Health check — confirms app config is loaded."""
    return {"app_name": settings.app_name}


@app.get("/chat")
def chat(question: str) -> dict:
    """
    Main chat endpoint. Checks Redis cache first to reduce LLM API costs.
    Falls back to LLM on cache miss and stores the result for future requests.
    """
    try:
        cache_key = get_cache_key(question)
        cached = get_cached_response(cache_key)
        if cached:
            logger.info(f"Cache HIT for key : {cache_key}")
            return {"source": "cache", "answer": cached}
        logger.info(f"Cache MISS for key: {cache_key}")
        llm_answer = call_llm(question)
        store_cached_response(cache_key, llm_answer)
        logger.info(f"Cached answer for key: {cache_key}")
        return {"source": "llm", "answer": llm_answer}
    except redis.RedisError as e:
        logger.error(f"Redis error during chat: {e}")
        return {
            "source": "llm",
            "answer": call_llm(question),
            "warning": "Cache unavailable",
        }
