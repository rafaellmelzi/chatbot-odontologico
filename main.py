import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from dotenv import load_dotenv

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

try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print('Twilio client initialized', file=sys.stderr)
except Exception as e:
    print(f'Twilio error: {e}', file=sys.stderr)
    client = None

@app.get('/')
async def root():
    return {'status': 'online'}

@app.get('/health')
async def health():
    return {'status': 'healthy'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    print('WEBHOOK CALLED', file=sys.stderr)
    try:
        form_data = await request.form()
        print(f'Form data keys: {list(form_data.keys())}', file=sys.stderr)
        
        incoming_msg = form_data.get('Body', '')
        sender = form_data.get('From', '')
        
        print(f'Message: "{incoming_msg}" from {sender}', file=sys.stderr)
        
        response_text = 'Ola! Bem-vindo!'
        
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=response_text,
            to=sender
        )
        print(f'Sent: {msg.sid}', file=sys.stderr)
        return PlainTextResponse('OK')
        
    except Exception as e:
        print(f'EXCEPTION: {str(e)}', file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return PlainTextResponse('OK')
