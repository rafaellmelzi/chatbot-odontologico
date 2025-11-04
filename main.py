from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Chatbot Odontologico',
    description='API para chatbot de consultório odontológico',
    version='1.0.0'
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
    return {
        'status': 'online',
        'message': 'Chatbot Odontologico API',
        'version': '1.0.0'
    }

@app.get('/health')
async def health():
    return {'status': 'healthy'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook():
    return {'received': True}

@app.get('/api/info')
async def api_info():
    return {
        'name': 'Chatbot Odontologico',
        'status': 'running',
        'features': ['WhatsApp Integration', 'Health Check']
    }
