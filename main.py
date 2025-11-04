import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from urllib.parse import parse_qs

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ULTRAMSG_INSTANCE = os.getenv('ULTRAMSG_INSTANCE', 'instance_id_aqui')
ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN', 'token_aqui')

@app.get('/')
async def root():
    return {'status': 'online'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    try:
        body = await request.body()
        data = parse_qs(body.decode('utf-8'))
        sender = data.get('From', [''])[0].replace('whatsapp:', '')
        
        url = f'https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/chat'
        
        response = requests.post(url, json={
            'token': ULTRAMSG_TOKEN,
            'to': sender,
            'body': 'Ola! Bem-vindo ao Chatbot Odontologico!'
        })
        
        print(f'Sent to {sender}', flush=True)
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'Error: {str(e)}', flush=True)
        return PlainTextResponse('OK')
