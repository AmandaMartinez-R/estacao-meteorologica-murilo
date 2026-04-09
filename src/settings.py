"""Porta e interfaces HTTP do Flask (app.py + URL do serial_reader)."""
import os

# Defina SERIAL_PORT no ambiente ou ajuste o fallback abaixo.
# A função escolher_porta() é responsável por escolher a porta serial correta, caso a função não encontre a porta serial, a função PORTA_FALLBACK é usada.

PORTA_FALLBACK = '/dev/ttyS4'
BAUD = 9600
# Mesma porta que app.run() (`export PORT=5001` se 5000 estiver ocupada)
URL = f'http://{API_CLIENT_HOST}:{FLASK_PORT}/leituras'


FLASK_PORT = int(os.environ.get('PORT', '5000'))
# Onde o servidor escuta (0.0.0.0 = aceitar da rede local)
FLASK_BIND_HOST = os.environ.get('FLASK_BIND_HOST', '127.0.0.1')
# Onde o serial_reader (na mesma máquina) envia o POST — use 127.0.0.1, não 0.0.0.0
API_CLIENT_HOST = os.environ.get('API_CLIENT_HOST', '127.0.0.1')
