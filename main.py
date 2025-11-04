import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from urllib.parse import parse_qs
import sys

# DEBUG: Print all env vars
print('=== ENV DEBUG ===', file=sys.stderr)
print(f'TWILIO_ACCOUNT_SID={os.getenv("TWILIO_ACCOUNT_SID")}', file=sys.stderr)
print(f'TWILIO_AUTH_TOKEN={os.getenv("TWILIO_AUTH_TOKEN")}', file=sys.stderr)
print(f'TWILIO_WHATSAPP_NUMBER={os.getenv("TWILIO_WHATSAPP_NUMBER")}', file=sys.stderr)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '')

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    print('WARNING: Twilio credentials missing!', file=sys.stderr)
    client = None

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
        
        print(f'Message from {sender}: {incoming_msg}', file=sys.stderr)
        
        if not client:
            print('No Twilio client!', file=sys.stderr)
            return PlainTextResponse('OK')
            
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body='Ola! Bem-vindo ao Chatbot Odontologico!',
            to=sender
        )
        print(f'Message sent: {msg.sid}', file=sys.stderr)
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'Exception: {e}', file=sys.stderr)
        return PlainTextResponse('OK')
