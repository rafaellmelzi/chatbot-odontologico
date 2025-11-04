import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from urllib.parse import parse_qs

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ULTRAMSG_INSTANCE = os.getenv('ULTRAMSG_INSTANCE', '')
ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN', '')

@app.get('/')
async def root():
    return {'status': 'online'}

@app.get('/health')
async def health():
    return {'status': 'healthy'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    try:
        body = await request.body()
        data = parse_qs(body.decode('utf-8'))
        sender = data.get('From', [''])[0].replace('whatsapp:', '')
        incoming = data.get('Body', [''])[0].lower()
        
        print(f'Message: {incoming} from {sender}', flush=True)
        
        if ULTRAMSG_INSTANCE and ULTRAMSG_TOKEN:
            url = f'https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/chat'
            
            response = requests.post(url, json={
                'token': ULTRAMSG_TOKEN,
                'to': sender,
                'body': 'Ola! Bem-vindo ao Chatbot Odontologico!'
            })
            
            print(f'Response: {response.status_code}', flush=True)
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'Error: {str(e)}', flush=True)
        return PlainTextResponse('OK')
