from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama

app = FastAPI(
    title="AI Code Assistant API",
    description="API powered by Ollama models (DeepSeek Coder & Qwen)",
    version="1.0.0"
)


# Pydantic models for request validation
class ChatRequest(BaseModel):
    message: str
    model: str = "qwen3:4b"  # default model


class CodeRequest(BaseModel):
    prompt: str
    language: str = "python"


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI Code Assistant API",
        "available_endpoints": ["/chat", "/code", "/models"],
        "docs": "/docs"
    }


# List available models
@app.get("/models")
def list_models():
    """Get list of available Ollama models"""
    try:
        models = ollama.list()
        return {
            "available_models": [model['name'] for model in models['models']],
            "count": len(models['models'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    """
    Chat with AI models
    - Use qwen2.5:4b for general questions
    - Use deepseek-coder:6.7b for coding questions
    """
    try:
        response = ollama.chat(
            model=request.model,
            messages=[
                {'role': 'user', 'content': request.message}
            ]
        )

        return {
            "model": request.model,
            "response": response['message']['content'],
            "done": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Code generation endpoint
@app.post("/code")
def generate_code(request: CodeRequest):
    """
    Generate code using DeepSeek Coder
    Automatically uses deepseek-coder:6.7b model
    """
    try:
        prompt = f"Write {request.language} code: {request.prompt}"

        response = ollama.chat(
            model='deepseek-coder:6.7b',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )

        return {
            "language": request.language,
            "prompt": request.prompt,
            "code": response['message']['content'],
            "model": "deepseek-coder:6.7b"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Code explanation endpoint
@app.post("/explain")
def explain_code(code: str):
    """Explain what a piece of code does"""
    try:
        prompt = f"Explain this code in simple terms:\n\n{code}"

        response = ollama.chat(
            model='deepseek-coder:6.7b',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )

        return {
            "explanation": response['message']['content'],
            "model": "deepseek-coder:6.7b"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")