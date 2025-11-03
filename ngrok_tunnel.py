from pyngrok import ngrok
import time

# Conectar ao localhost:8000
public_url = ngrok.connect(8000)
print(f"🌐 URL PÚBLICA: {public_url}")
print(f"✅ Seu servidor está online em: {public_url}/")
print("\nPressione Ctrl+C para desconectar...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n❌ Desconectado!")
