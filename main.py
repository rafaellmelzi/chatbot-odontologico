import os
import http.client
import ssl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from urllib.parse import parse_qs
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ULTRAMSG_INSTANCE = os.getenv('ULTRAMSG_INSTANCE', '')
ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN', '')

@app.get('/')
async def root():
    return {'status': 'online'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    try:
        body = await request.body()
        data = parse_qs(body.decode('utf-8'))
        
        # Ultramsg envia como form data
        sender = data.get('phone', [''])[0] or data.get('to', [''])[0]
        incoming = data.get('body', [''])[0]
        
        print(f'Received: {incoming} from {sender}', flush=True)
        print(f'Data: {data}', flush=True)
        
        if sender and ULTRAMSG_INSTANCE and ULTRAMSG_TOKEN:
            conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
            
            # Formata o número com whatsapp:
            if not sender.startswith('whatsapp:'):
                sender_formatted = f'whatsapp:{sender}'
            else:
                sender_formatted = sender
            
            payload = f"token={ULTRAMSG_TOKEN}&to={sender_formatted}&body=Ola! Bem-vindo ao Chatbot Odontologico!"
            payload = payload.encode('utf8').decode('iso-8859-1')
            
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            
            conn.request("POST", f"/{ULTRAMSG_INSTANCE}/messages/chat", payload, headers)
            res = conn.getresponse()
            result = res.read()
            
            print(f'Sent: {result.decode("utf-8")}', flush=True)
        else:
            print(f'Missing sender or credentials', flush=True)
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'Error: {str(e)}', flush=True)
        import traceback
        traceback.print_exc()
        return PlainTextResponse('OK')
