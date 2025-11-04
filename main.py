import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from dotenv import load_dotenv
from urllib.parse import parse_qs

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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
        incoming_msg = data.get('Body', [''])[0].lower()
        sender = data.get('From', [''])[0]
        
        msg = client.messages.create(from_=TWILIO_WHATSAPP_NUMBER, body='Ola! Bem-vindo!', to=sender)
        return PlainTextResponse('OK')
    except:
        return PlainTextResponse('OK')
