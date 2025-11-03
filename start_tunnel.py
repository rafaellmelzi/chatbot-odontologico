import subprocess
from pyngrok import ngrok

print("Starting Cloudflare Tunnel...")
try:
    # Configure ngrok authtoken (use seu token se tiver)
    public_url = ngrok.connect(8000)
    print(f"Tunnel URL: {public_url}")
    print("Press Ctrl+C to stop")
    ngrok_process = ngrok.get_ngrok_process()
    ngrok_process.proc.wait()
except Exception as e:
    print(f"Error: {e}")
