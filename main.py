import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from twilio.request_validator import RequestValidator
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

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
validator = RequestValidator(TWILIO_AUTH_TOKEN)

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

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    \"\"\"Webhook para receber mensagens do WhatsApp via Twilio\"\"\"
    try:
        # Obtém parâmetros do formulário
        form_data = await request.form()
        incoming_msg = form_data.get('Body', '').lower()
        sender = form_data.get('From', '')
        
        print(f'Mensagem recebida: {incoming_msg} de {sender}')
        
        # Lógica de resposta
        if 'oi' in incoming_msg or 'olá' in incoming_msg or 'oi' == incoming_msg:
            response_text = 'Olá! Bem-vindo ao Chatbot Odontológico! 😊\\n\\nComo posso ajudar?\\n• Horários\\n• Informações gerais\\n• Agendar consulta'
        elif 'horário' in incoming_msg:
            response_text = '🕐 Nosso horário é:\\n📅 Segunda a Sexta: 8h - 18h\\n📅 Sábado: 8h - 12h\\n\\nFechado aos domingos!'
        elif 'preço' in incoming_msg or 'valor' in incoming_msg or 'cust' in incoming_msg:
            response_text = '💰 Para consultar valores, por favor ligue:\\n📞 (31) 9999-9999'
        elif 'agendar' in incoming_msg or 'consulta' in incoming_msg:
            response_text = '📅 Para agendar sua consulta:\\n📞 Ligue: (31) 9999-9999\\n💬 Ou nos envie uma mensagem com:\\n- Seu nome\\n- Data preferida'
        else:
            response_text = '👋 Desculpe, não entendi muito bem.\\n\\nPosso ajudar com:\\n• Horários 🕐\\n• Preços 💰\\n• Agendamento 📅'
        
        # Envia resposta via Twilio
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=response_text,
            to=sender
        )
        
        print(f'Resposta enviada: {message.sid}')
        return PlainTextResponse('OK')
        
    except Exception as e:
        print(f'Erro: {str(e)}')
        return PlainTextResponse('ERROR', status_code=400)
