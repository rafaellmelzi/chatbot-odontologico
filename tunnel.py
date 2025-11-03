import time
print('Tunnel habilitado em: http://localhost:8000')
print('Pressione Ctrl+C para sair')
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\nSaindo...')
