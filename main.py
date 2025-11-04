import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from urllib.parse import parse_qs

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

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
        sender = data.get('From', [''])[0]
        
        sid = os.getenv('TWILIO_ACCOUNT_SID')
        token = os.getenv('TWILIO_AUTH_TOKEN')
        whatsapp_from = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        print(f'WEBHOOK: Received from {sender}', flush=True)
        
        if sid and token and whatsapp_from:
            try:
                client = Client(sid, token)
                msg = client.messages.create(from_=whatsapp_from, body='Ola! Funciona!', to=sender)
                print(f'SUCCESS: Message sent {msg.sid}', flush=True)
            except Exception as e:
                print(f'SEND ERROR: {str(e)}', flush=True)
        else:
            print('MISSING CREDENTIALS', flush=True)
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'ERROR: {str(e)}', flush=True)
        return PlainTextResponse('OK')
