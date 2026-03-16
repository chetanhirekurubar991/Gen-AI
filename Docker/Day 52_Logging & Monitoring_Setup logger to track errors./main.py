import structlog
from fastapi import FastAPI
app=FastAPI()

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger=structlog.get_logger()
@app.get('/')
def root():
    logger.info('user_login')
    return {'message':'hello world'}

@app.post('/chat')
def chat(messages:str):
    logger.info('chat_request_received',message_length=len(messages))
    return {'reply':'I Hear You'}
