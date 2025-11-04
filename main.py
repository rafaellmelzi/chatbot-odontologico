from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online", "message": "Chatbot Odontologico API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/webhook/whatsapp")
async def whatsapp_webhook():
    return {"received": True}
