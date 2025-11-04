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

# Base de conhecimento odontológica
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
    'branqueamento': 'Temos clareamento dental profissional com resultado em poucas sessões! ✨',
}

def detectar_intencao(mensagem):
    """Detecta a intenção da mensagem do usuário"""
    msg = mensagem.lower().strip()
    
    # Intenção: Saudação
    if any(word in msg for word in ['oi', 'ola', 'olá', 'e aí', 'tudo bem', 'oi!']):
        return 'saudacao'
    
    # Intenção: Implante
    if any(word in msg for word in ['implante', 'implantes', 'implanta']):
        return 'implante'
    
    # Intenção: Clareamento/Branqueamento
    if any(word in msg for word in ['clareamento', 'branqueamento', 'branco', 'claro']):
        return 'clareamento'
    
    # Intenção: Canal
    if any(word in msg for word in ['canal', 'endodontia', 'dor de dente']):
        return 'canal'
    
    # Intenção: Limpeza
    if any(word in msg for word in ['limpeza', 'profilaxia', 'higiene']):
        return 'limpeza'
    
    # Intenção: Gengivite
    if any(word in msg for word in ['gengivite', 'gengiva', 'sangra']):
        return 'gengivite'
    
    # Intenção: Horário
    if any(word in msg for word in ['horário', 'horario', 'funciona', 'abre', 'fecha']):
        return 'horário'
    
    # Intenção: Preço
    if any(word in msg for word in ['preço', 'preco', 'valor', 'custa', 'costo']):
        return 'preço'
    
    # Intenção: Agendar
    if any(word in msg for word in ['agendar', 'marcar', 'consulta', 'agendamento']):
        return 'agendar'
    
    # Intenção: Emergência
    if any(word in msg for word in ['emergência', 'emergencia', 'urgência', 'urgencia', 'dor']):
        return 'emergência'
    
    return 'padrao'

def gerar_resposta(intencao):
    """Gera resposta baseada na intenção detectada"""
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

def enviar_resposta(sender, resposta):
    """Envia resposta para o Ultramsg"""
    try:
        if not sender.startswith('whatsapp:'):
            sender_formatted = f'whatsapp:{sender}'
        else:
            sender_formatted = sender
        
        conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
        payload = f"token={ULTRAMSG_TOKEN}&to={sender_formatted}&body={resposta}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        conn.request("POST", f"/{ULTRAMSG_INSTANCE}/messages/chat", payload, headers)
        res = conn.getresponse()
        result = res.read()
        
        print(f'Response: {result.decode("utf-8")}', flush=True)
        return True
    except Exception as e:
        print(f'Erro ao enviar: {str(e)}', flush=True)
        return False

@app.get('/')
async def root():
    return {'status': 'online'}

@app.post('/webhook/whatsapp')
async def whatsapp_webhook(request: Request):
    try:
        body = await request.body()
        data = parse_qs(body.decode('utf-8'))
        
        sender = data.get('phone', [''])[0].strip()
        mensagem = data.get('body', [''])[0].strip()
        
        print(f'📱 Mensagem recebida: "{mensagem}" de {sender}', flush=True)
        
        # Detecta intenção
        intencao = detectar_intencao(mensagem)
        print(f'🔍 Intenção detectada: {intencao}', flush=True)
        
        # Gera resposta
        resposta = gerar_resposta(intencao)
        print(f'💬 Resposta: {resposta}', flush=True)
        
        # Envia resposta
        if ULTRAMSG_INSTANCE and ULTRAMSG_TOKEN:
            enviar_resposta(sender, resposta)
        
        return PlainTextResponse('OK')
    except Exception as e:
        print(f'❌ Erro: {str(e)}', flush=True)
        import traceback
        traceback.print_exc()
        return PlainTextResponse('OK')
