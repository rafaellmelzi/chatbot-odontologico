import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from dotenv import load_dotenv
import traceback

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

print(f'TWILIO_WHATSAPP_NUMBER: {TWILIO_WHATSAPP_NUMBER}')

try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
except Exception as e:
    print(f'Erro ao conectar Twilio: {e}')
    client = None

@app.get('/')
async def root():
    return {'status': 'online', 'message': 'Chatbot Odontologico API'}

@app.get('/health')
async def health():
    return {'status': 'healthy'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    try:
        form_data = await request.form()
        incoming_msg = form_data.get('Body', '').lower().strip()
        sender = form_data.get('From', '')
        
        print(f'DEBUG: Mensagem: "{incoming_msg}" | De: {sender}')
        
        if not sender or not incoming_msg:
            print('DEBUG: Campos vazio')
            return PlainTextResponse('OK')
        
        response_text = 'Ola! Bem-vindo ao Chatbot Odontologico!'
        
        if client:
            msg = client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=response_text,
                to=sender
            )
            print(f'DEBUG: Mensagem enviada: {msg.sid}')
        else:
            print('DEBUG: Cliente Twilio nao disponivel')
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'ERROR: {str(e)}')
        traceback.print_exc()
        return PlainTextResponse('OK')
