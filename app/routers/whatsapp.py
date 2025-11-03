from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from app.services.chatbot_service import chatbot_service
from app.core.config import settings
from twilio.rest import Client

router = APIRouter(prefix="/webhook", tags=["WhatsApp"])

# Inicializar cliente Twilio
twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


@router.post("/whatsapp")
async def handle_whatsapp_message(request: Request):
    """
    Recebe mensagens do WhatsApp via Twilio
    Processa com IA e envia resposta de volta
    """
    try:
        # Extrair dados do formulário enviado pelo Twilio
        form_data = await request.form()
        from_number = form_data.get("From", "")  # whatsapp:+55...
        message_text = form_data.get("Body", "").strip()
        
        logger.info(f"📱 Mensagem recebida de {from_number}: {message_text}")
        
        # Validar se tem mensagem
        if not message_text:
            logger.warning("⚠️ Mensagem vazia recebida")
            return {"status": "ok"}
        
        # Gerar resposta com IA (Google Gemini)
        logger.info("🤖 Processando com IA...")
        ai_response = await chatbot_service.generate_response(message_text)
        logger.info(f"✅ IA respondeu: {ai_response[:100]}...")
        
        # Enviar resposta de volta via Twilio
        message = twilio_client.messages.create(
            body=ai_response,
            from_=settings.TWILIO_WHATSAPP_FROM,  # whatsapp:+14155238886
            to=from_number  # Número do cliente
        )
        
        logger.info(f"✅ Mensagem enviada com sucesso: {message.sid}")
        
        return {
            "status": "success",
            "message_id": message.sid,
            "response": ai_response
        }
    
    except Exception as e:
        logger.error(f"❌ ERRO ao processar mensagem: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "error": str(e)
        }


@router.get("/whatsapp")
async def verify_webhook():
    """
    Endpoint para verificar se o webhook está funcionando
    Usado pelo Twilio durante a configuração
    """
    logger.info("✅ Webhook verificado com sucesso")
    return {
        "status": "ok",
        "message": "Webhook do WhatsApp está ativo"
    }
