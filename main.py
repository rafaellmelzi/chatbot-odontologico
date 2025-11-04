import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = FastAPI(title='Chatbot Odontologico', version='1.0.0')

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Configuração Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

print(f'TWILIO_ACCOUNT_SID: {TWILIO_ACCOUNT_SID[:10]}...', file=sys.stderr)
print(f'TWILIO_WHATSAPP_NUMBER: {TWILIO_WHATSAPP_NUMBER}', file=sys.stderr)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.get('/')
async def root():
    return {'status': 'online', 'message': 'Chatbot Odontologico API', 'version': '1.0.0'}

@app.get('/health')
async def health():
    return {'status': 'healthy'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    try:
        form_data = await request.form()
        incoming_msg = form_data.get('Body', '').lower()
        sender = form_data.get('From', '')
        
        print(f'[DEBUG] Mensagem: {incoming_msg} | De: {sender}', file=sys.stderr)
        
        # Resposta simples
        response_text = 'Olá! Bem-vindo ao Chatbot Odontológico! 😊'
        
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=response_text,
            to=sender
        )
        
        print(f'[DEBUG] Resposta enviada: {msg.sid}', file=sys.stderr)
        return PlainTextResponse('OK')
        
    except Exception as e:
        print(f'[ERROR] {str(e)}', file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return PlainTextResponse('ERROR', status_code=400)
