# Defina SERIAL_PORT no ambiente ou ajuste o fallback abaixo.
# A função escolher_porta() é responsável por escolher a porta serial correta, caso a função não encontre a porta serial, a função PORTA_FALLBACK é usada.
PORTA_FALLBACK = '/dev/ttyS4'
BAUD = 9600
URL = 'http://localhost:5000/leituras'
