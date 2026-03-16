from fastapi import FastAPI
from config import settings
app=FastAPI(docs_url='/chetan')
@app.get('/')
def root():
    return {'app_name':settings.app_name}