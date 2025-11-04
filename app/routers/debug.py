from fastapi import APIRouter
from loguru import logger
import httpx
import json

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/test-openai-direct")
async def test_openai_direct():
    """Testa OpenAI diretamente e registra tudo em detalhes"""
    
    logger.info("=" * 100)
    logger.info("🧪 TESTE OPENAI DIRETO - INICIANDO")
    logger.info("=" * 100)
    
    try:
        # ===== PASSO 1: Configurar chave =====
        logger.info("\n📋 PASSO 1: Configurando chave OpenAI")
        api_key = "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"
        logger.info(f"✅ Chave carregada: {api_key[:30]}...{api_key[-10:]}")
        logger.info(f"✅ Comprimento da chave: {len(api_key)} caracteres")
        
        # ===== PASSO 2: Configurar URL =====
        logger.info("\n📋 PASSO 2: Configurando URL da API")
        url = "https://api.openai.com/v1/chat/completions"
        logger.info(f"✅ URL: {url}")
        
        # ===== PASSO 3: Preparar headers =====
        logger.info("\n📋 PASSO 3: Preparando headers")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        logger.info(f"✅ Authorization header: Bearer {api_key[:20]}...")
        logger.info(f"✅ Content-Type: application/json")
        
        # ===== PASSO 4: Preparar payload =====
        logger.info("\n📋 PASSO 4: Preparando payload")
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é Luna, assistente de uma clínica odontológica. Responda em português brasileiro, de forma breve (máximo 3 linhas), amigável e profissional."
                },
                {
                    "role": "user",
                    "content": "Olá! Como você pode me ajudar?"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        logger.info(f"✅ Model: {payload['model']}")
        logger.info(f"✅ Mensagens: {len(payload['messages'])} mensagens")
        logger.info(f"✅ Payload JSON preparado com sucesso")
        
        # ===== PASSO 5: Enviar requisição =====
        logger.info("\n📋 PASSO 5: Enviando requisição para OpenAI")
        logger.info(f"🚀 Iniciando conexão com {url}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.info("✅ Cliente HTTP async criado")
            logger.info("🌐 Enviando POST request...")
            
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            # ===== PASSO 6: Analisar resposta =====
            logger.info("\n📋 PASSO 6: Analisando resposta")
            logger.info(f"✅ Resposta recebida!")
            logger.info(f"✅ Status HTTP: {response.status_code}")
            
            response_text = response.text
            logger.info(f"\n📄 Corpo da resposta (primeiros 500 chars):")
            logger.info(f"{response_text[:500]}")
            
            # ===== PASSO 7: Processar resultado =====
            logger.info("\n📋 PASSO 7: Processando resultado")
            
            if response.status_code == 200:
                logger.info("✅ Status 200 OK!")
                result = response.json()
                logger.info(f"✅ JSON parseado com sucesso")
                
                ai_message = result['choices'][0]['message']['content']
                logger.info(f"✅ Resposta IA: {ai_message}")
                
                logger.info("\n" + "=" * 100)
                logger.info("✅✅✅ TESTE CONCLUÍDO COM SUCESSO! ✅✅✅")
                logger.info("=" * 100)
                
                return {
                    "status": "✅ SUCESSO TOTAL",
                    "http_status": 200,
                    "ai_response": ai_message,
                    "message": "A API OpenAI está funcionando perfeitamente!"
                }
            
            elif response.status_code == 401:
                logger.error(f"\n❌ ERRO 401: Unauthorized")
                logger.error(f"❌ A chave API pode estar inválida ou expirada")
                
                return {
                    "status": "❌ ERRO 401 - UNAUTHORIZED",
                    "http_status": 401,
                    "error": response_text,
                    "message": "Chave API inválida ou expirada"
                }
            
            else:
                logger.error(f"\n❌ ERRO HTTP {response.status_code}")
                logger.error(f"❌ Resposta: {response_text}")
                
                return {
                    "status": f"❌ ERRO HTTP {response.status_code}",
                    "http_status": response.status_code,
                    "error": response_text,
                    "message": f"Problema ao conectar com OpenAI (HTTP {response.status_code})"
                }
    
    except httpx.TimeoutException as e:
        logger.error(f"\n❌ TIMEOUT")
        logger.error(f"❌ Erro: {str(e)}")
        
        return {
            "status": "❌ TIMEOUT",
            "error": "Requisição demorou mais de 30 segundos",
            "message": "A API OpenAI está muito lenta"
        }
    
    except Exception as e:
        logger.error(f"\n❌ EXCEÇÃO GERAL")
        logger.error(f"❌ Tipo: {type(e).__name__}")
        logger.error(f"❌ Mensagem: {str(e)}")
        import traceback
        logger.error(f"\n❌ Traceback:\n{traceback.format_exc()}")
        
        return {
            "status": "❌ ERRO GERAL",
            "error": str(e),
            "type": type(e).__name__,
            "message": "Verifique o arquivo debug.log para mais detalhes"
        }


@router.get("/logs")
async def get_logs():
    """Retorna os últimos logs"""
    logger.info("📋 Endpoint /debug/logs acessado")
    
    try:
        with open("debug.log", "r", encoding="utf-8") as f:
            logs_content = f.read()
        
        lines = logs_content.split("\n")
        recent_logs = "\n".join(lines[-50:])
        
        logger.info(f"✅ Retornando {len(lines)} linhas de log")
        
        return {
            "status": "✅ Logs carregados",
            "total_lines": len(lines),
            "recent_logs": recent_logs
        }
    
    except FileNotFoundError:
        logger.error("❌ Arquivo debug.log não encontrado")
        return {
            "status": "❌ Arquivo não encontrado",
            "error": "Execute /debug/test-openai-direct primeiro"
        }
    
    except Exception as e:
        logger.error(f"❌ Erro ao ler logs: {str(e)}")
        return {
            "status": "❌ Erro",
            "error": str(e)
        }


@router.get("/status")
async def debug_status():
    """Retorna status do debug"""
    logger.info("📊 /debug/status acessado")
    
    return {
        "status": "🟢 Debug ativo",
        "endpoints": {
            "test": "/debug/test-openai-direct",
            "logs": "/debug/logs",
            "status": "/debug/status"
        }
    }
