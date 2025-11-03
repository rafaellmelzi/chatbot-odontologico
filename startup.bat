@echo off
chcp 65001 >nul
title Chatbot Odontologico - Startup

echo ========================================
echo Iniciando Chatbot Odontologico
echo ========================================
echo.

REM Verificar se Python est? instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Python nao encontrado!
    pause
    exit /b 1
)

REM Instalar dependencias
echo [1/3] Instalando dependencias...
pip install -r requirements.txt >nul 2>&1

REM Configurar ngrok token
echo [2/3] Configurando ngrok...
python -c "from pyngrok import ngrok; ngrok.set_auth_token('34ygKsmfOkvFJy6iEwe3Kl9h8Xx_i8a3n7SDHZTysnEwEADm')" >nul 2>&1

REM Iniciar aplicacao
echo [3/3] Iniciando servidor...
echo.
echo ========================================
echo Servidor online em: http://localhost:8000
echo Pressione Ctrl+C para parar
echo ========================================
echo.

python -m uvicorn app.main:app --reload

pause
