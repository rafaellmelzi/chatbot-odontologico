import os
import http.client
import ssl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from urllib.parse import parse_qs
import urllib.parse
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
        
        # Debug completo
        print('='*50, flush=True)
        print(f'RAW BODY: {body}', flush=True)
        print(f'RAW BODY (hex): {body.hex()}', flush=True)
        
        # Tenta diferentes encodings
        try:
            text = body.decode('utf-8')
            print(f'✅ UTF-8 OK', flush=True)
        except:
            text = body.decode('iso-8859-1')
            print(f'✅ ISO-8859-1 OK', flush=True)
        
        print(f'TEXT: {text}', flush=True)
        
        data = parse_qs(text)
        print(f'PARSED DATA: {data}', flush=True)
        print(f'ALL KEYS: {list(data.keys())}', flush=True)
        print('='*50, flush=True)
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'❌ Erro: {str(e)}', flush=True)
        import traceback
        traceback.print_exc()
        return PlainTextResponse('OK')
