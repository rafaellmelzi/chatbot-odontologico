from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.chatbot_service import chatbot_service

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Online", "ai": "Gemini 2.0 Flash"}

@app.get("/gemini-test")
async def gemini_test():
    response = await chatbot_service.generate_response("Olá")
    return {"response": response}

@app.post("/chat")
async def chat(message: str):
    """Endpoint para testar chatbot"""
    response = await chatbot_service.generate_response(message)
    return {"message": message, "response": response}

@app.get("/docs")
async def docs():
    return {"docs": "/docs", "redoc": "/redoc"}
