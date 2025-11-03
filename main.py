from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Chatbot Online!", "status": "OK"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/webhook/whatsapp")
def whatsapp_webhook(request: dict):
    return {"received": True}

# Deploy fix - 2025-11-03 16:26:10
