import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from dotenv import load_dotenv
from urllib.parse import parse_qs

load_dotenv()

app = FastAPI(title='Chatbot Odontologico', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

print(f'Loaded: {TWILIO_WHATSAPP_NUMBER}')

try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
except Exception as e:
    print(f'Error: {e}')
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
        
        incoming_msg = data.get('Body', [''])[0].lower().strip()
        sender = data.get('From', [''])[0]
        
        print(f'Message: {incoming_msg} from {sender}')
        
        response_text = 'Ola! Bem-vindo ao Chatbot Odontologico!'
        
        if client and sender:
            msg = client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=response_text,
                to=sender
            )
            print(f'Sent: {msg.sid}')
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'Error: {e}')
        return PlainTextResponse('OK')
