import subprocess
import time
import os

print("🌐 Iniciando Cloudflare Tunnel...")
print("Conectando ao localhost:8000...")

os.system("cloudflared tunnel --url http://localhost:8000")
