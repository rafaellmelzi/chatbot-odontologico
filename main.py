import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

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

# Configuração Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
USER_WHATSAPP_NUMBER = os.getenv('USER_WHATSAPP_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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

@app.get('/api/info')
async def api_info():
    return {
        'name': 'Chatbot Odontologico',
        'status': 'running',
        'features': ['WhatsApp Integration', 'Health Check']
    }

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    \"\"\"Recebe mensagens do WhatsApp via Twilio\"\"\"
    try:
        form_data = await request.form()
        incoming_msg = form_data.get('Body', '')
        sender = form_data.get('From', '')
        
        # Respostas automáticas
        if 'oi' in incoming_msg.lower() or 'olá' in incoming_msg.lower():
            response_text = 'Olá! Bem-vindo ao Chatbot Odontológico! Como posso ajudar?'
        elif 'horário' in incoming_msg.lower():
            response_text = 'Nosso horário é: Segunda a Sexta 8h-18h, Sábado 8h-12h'
        elif 'preço' in incoming_msg.lower() or 'valor' in incoming_msg.lower():
            response_text = 'Para consultar valores, por favor ligue: (31) 9999-9999'
        else:
            response_text = 'Desculpe, não entendi. Posso ajudar com:\n• Horários\n• Informações gerais'
        
        # Envia resposta via Twilio
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=response_text,
            to=sender
        )
        
        return {'received': True, 'message_sid': message.sid}
    except Exception as e:
        return {'error': str(e)}

@app.post('/send-message')
async def send_message(message: dict):
    \"\"\"Endpoint para enviar mensagens manualmente\"\"\"
    try:
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message.get('text', 'Teste'),
            to=message.get('to', USER_WHATSAPP_NUMBER)
        )
        return {'sent': True, 'sid': msg.sid}
    except Exception as e:
        return {'error': str(e)}
