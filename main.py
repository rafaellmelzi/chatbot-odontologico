import os
import http.client
import ssl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import json
import urllib.parse
import requests
import time

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ULTRAMSG_INSTANCE = os.getenv('ULTRAMSG_INSTANCE', '')
ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# WHITELIST - números e grupos permitidos
NUMEROS_PERMITIDOS = [
    '5516991190909',           # Seu número
    '120363402544453088',      # ID do grupo
]

def gerar_resposta_gemini(mensagem):
    """Gera resposta com Google Gemini AI"""
    try:
        print('🤖 Gemini processando...', flush=True)
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        
        contexto = f"""Você é um assistente de clínica odontológica em Barreiro, Belo Horizonte.

INFORMAÇÕES:
- Telefone: (31) 99119-0909
- Horário: Segunda a sexta 08:00-18:00, Sábado até 13:00
- Especialidades: Implantes, Clareamento, Canal, Limpeza, Gengivite

Pergunta do cliente: {mensagem}

RESPONDA: Em até 3 linhas, de forma profissional e amigável."""
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": contexto
                }]
            }]
        }
        
        response = requests.post(
            f"{url}?key={GEMINI_API_KEY}",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            resposta = result['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Limita a 200 caracteres
            if len(resposta) > 200:
                resposta = resposta[:200] + '...'
            
            return resposta
        else:
            return '📞 Erro ao processar. Ligue: (31) 99119-0909'
    
    except Exception as e:
        print(f'❌ Erro Gemini: {str(e)}', flush=True)
        return '📞 Desculpe, ocorreu um erro. Ligue: (31) 99119-0909'

def enviar_resposta(sender_number, resposta):
    """Envia resposta via Ultramsg"""
    try:
        numero = sender_number.replace('@c.us', '').replace('@g.us', '')
        sender_formatted = f'whatsapp:{numero}'
        
        conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
        
        resposta_encoded = urllib.parse.quote(resposta)
        payload = f"token={ULTRAMSG_TOKEN}&to={sender_formatted}&body={resposta_encoded}"
        
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        conn.request("POST", f"/{ULTRAMSG_INSTANCE}/messages/chat", payload, headers)
        res = conn.getresponse()
        result = res.read()
        
        print(f'✅ Resposta enviada: {result.decode("utf-8")}', flush=True)
        return True
    except Exception as e:
        print(f'❌ Erro ao enviar: {str(e)}', flush=True)
        return False

@app.get('/')
async def root():
    return {
        'status': 'online',
        'bot': 'WhatsApp + Gemini AI',
        'version': '2.0'
    }

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    """Webhook que recebe mensagens do WhatsApp"""
    try:
        body = await request.body()
        
        try:
            text = body.decode('utf-8')
        except:
            text = body.decode('iso-8859-1')
        
        if text.startswith('{'):
            data = json.loads(text)
            evento = data.get('event_type')
            
            if evento == 'message_received':
                msg_data = data.get('data', {})
                sender = msg_data.get('from', '')
                mensagem = msg_data.get('body', '').strip()
                
                print(f'📱 Mensagem: "{mensagem}" de {sender}', flush=True)
                
                # Extrai número/grupo
                numero = sender.replace('@c.us', '').replace('@g.us', '')
                
                # Verifica permissão
                if numero not in NUMEROS_PERMITIDOS:
                    print(f'🚫 Número NÃO permitido: {numero}', flush=True)
                    return PlainTextResponse('OK')
                
                print(f'✅ Número autorizado: {numero}', flush=True)
                
                if not mensagem:
                    print(f'⏭️ Mensagem vazia', flush=True)
                    return PlainTextResponse('OK')
                
                # Gera resposta com Gemini
                resposta = gerar_resposta_gemini(mensagem)
                
                print(f'💬 Resposta: {resposta}', flush=True)
                
                # Aguarda 1 segundo antes de enviar
                time.sleep(1)
                
                # Envia resposta
                if ULTRAMSG_INSTANCE and ULTRAMSG_TOKEN:
                    enviar_resposta(sender, resposta)
        
        return PlainTextResponse('OK')
    
    except Exception as e:
        print(f'❌ Erro webhook: {str(e)}', flush=True)
        import traceback
        traceback.print_exc()
        return PlainTextResponse('OK')
