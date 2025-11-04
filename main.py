import os
import http.client
import ssl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import json
import urllib.parse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ULTRAMSG_INSTANCE = os.getenv('ULTRAMSG_INSTANCE', '')
ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN', '')

RESPOSTAS = {
    'implante': 'Nossos implantes dentários são feitos com os melhores materiais. Agende uma consulta! 📞',
    'clareamento': 'Temos clareamento dental profissional com resultado em poucas sessões! ✨',
    'canal': 'Tratamento de canal indolor com tecnologia avançada. Marque sua consulta!',
    'limpeza': 'Limpeza profunda e completa para manter seus dentes saudáveis. 🦷',
    'gengivite': 'Tratamento eficaz para gengivite. Procure nosso periodontista!',
    'horário': 'Abrimos de segunda a sexta, 08:00 às 18:00. Sábados até 13:00.',
    'preço': 'Temos planos flexíveis e financiamento. Fale com nosso atendente!',
    'agendar': 'Para agendar, responda com: DATA e HORÁRIO desejado',
    'emergência': 'Realizamos atendimentos de emergência 24h! Ligue 📞',
}

def detectar_intencao(mensagem):
    msg = mensagem.lower().strip()
    
    if any(word in msg for word in ['oi', 'ola', 'olá', 'e aí', 'tudo bem', 'opa', 'ta bom']):
        return 'saudacao'
    if any(word in msg for word in ['implante', 'implantes']):
        return 'implante'
    if any(word in msg for word in ['clareamento', 'branqueamento', 'branco']):
        return 'clareamento'
    if any(word in msg for word in ['canal', 'endodontia']):
        return 'canal'
    if any(word in msg for word in ['limpeza', 'profilaxia']):
        return 'limpeza'
    if any(word in msg for word in ['gengivite', 'gengiva']):
        return 'gengivite'
    if any(word in msg for word in ['horário', 'horario', 'funciona']):
        return 'horário'
    if any(word in msg for word in ['preço', 'preco', 'valor']):
        return 'preço'
    if any(word in msg for word in ['agendar', 'marcar', 'consulta']):
        return 'agendar'
    if any(word in msg for word in ['emergência', 'emergencia', 'urgência', 'dor']):
        return 'emergência'
    
    return 'padrao'

def gerar_resposta(intencao):
    respostas_intencao = {
        'saudacao': '👋 Bem-vindo! Sou o Chatbot da Clínica Odontológica. Como posso ajudar? 😊',
        'implante': RESPOSTAS['implante'],
        'clareamento': RESPOSTAS['clareamento'],
        'canal': RESPOSTAS['canal'],
        'limpeza': RESPOSTAS['limpeza'],
        'gengivite': RESPOSTAS['gengivite'],
        'horário': RESPOSTAS['horário'],
        'preço': RESPOSTAS['preço'],
        'agendar': RESPOSTAS['agendar'],
        'emergência': RESPOSTAS['emergência'],
        'padrao': '📞 Não entendi direito. Você pode me perguntar sobre: Implantes, Clareamento, Canal, Limpeza, Horários ou Agendamento?'
    }
    return respostas_intencao.get(intencao, respostas_intencao['padrao'])

def enviar_resposta(sender_number, resposta):
    try:
        # Remove @c.us e adiciona whatsapp:
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
    return {'status': 'online'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    try:
        body = await request.body()
        
        try:
            text = body.decode('utf-8')
        except:
            text = body.decode('iso-8859-1')
        
        # Verifica se é JSON (Ultramsg) ou form-data
        if text.startswith('{'):
            # É JSON
            data = json.loads(text)
            evento = data.get('event_type')
            
            if evento == 'message_received':
                msg_data = data.get('data', {})
                sender = msg_data.get('from', '')
                mensagem = msg_data.get('body', '')
                
                print(f'📱 Mensagem: "{mensagem}" de {sender}', flush=True)
                
                if sender and mensagem:
                    intencao = detectar_intencao(mensagem)
                    print(f'🔍 Intenção: {intencao}', flush=True)
                    
                    resposta = gerar_resposta(intencao)
                    print(f'💬 Resposta: {resposta}', flush=True)
                    
                    if ULTRAMSG_INSTANCE and ULTRAMSG_TOKEN:
                        enviar_resposta(sender, resposta)
        else:
            # É form-data (teste manual)
            from urllib.parse import parse_qs
            form_data = parse_qs(text)
            sender = form_data.get('phone', [''])[0]
            mensagem = form_data.get('body', [''])[0]
            
            print(f'📱 Teste: "{mensagem}" de {sender}', flush=True)
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'❌ Erro: {str(e)}', flush=True)
        import traceback
        traceback.print_exc()
        return PlainTextResponse('OK')
