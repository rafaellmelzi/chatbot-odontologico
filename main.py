import os
import http.client
import ssl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from urllib.parse import parse_qs

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ULTRAMSG_INSTANCE = os.getenv('ULTRAMSG_INSTANCE', '')
ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN', '')

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
        sender = data.get('From', [''])[0].replace('whatsapp:', '')
        incoming = data.get('Body', [''])[0]
        
        print(f'Received: {incoming} from {sender}', flush=True)
        
        if ULTRAMSG_INSTANCE and ULTRAMSG_TOKEN:
            conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
            
            payload = f"token={ULTRAMSG_TOKEN}&to={sender}&body=Ola! Bem-vindo ao Chatbot Odontologico!"
            payload = payload.encode('utf8').decode('iso-8859-1')
            
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            
            conn.request("POST", f"/{ULTRAMSG_INSTANCE}/messages/chat", payload, headers)
            res = conn.getresponse()
            data = res.read()
            
            print(f'Response: {data.decode("utf-8")}', flush=True)
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'Error: {str(e)}', flush=True)
        return PlainTextResponse('OK')
