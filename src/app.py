from datetime import datetime

from flask import Flask, request, jsonify, render_template

from database import *
from settings import FLASK_BIND_HOST, FLASK_PORT

app = Flask(__name__)

# Se a última leitura for mais antiga que isso, consideramos o fluxo serial/API parado
# (firmware envia a cada ~5 s; margem para atrasos de rede/USB)
HEARTBEAT_MAX_AGE_SEC = 25

# inicializa banco ao subir o servidor
init_db()


def compute_serial_heartbeat(leituras):
    """Indica se dados novos estão chegando (última linha no banco é recente)."""
    if not leituras:
        return {
            'ok': False,
            'ultima': None,
            'segundos': None,
            'mensagem': 'Nenhuma leitura — ligue o Arduino e o serial_reader',
        }
    raw = leituras[0]['timestamp']
    dt = None
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
        try:
            dt = datetime.strptime(str(raw), fmt)
            break
        except ValueError:
            continue
    if dt is None:
        return {
            'ok': False,
            'ultima': str(raw),
            'segundos': None,
            'mensagem': 'Horário da última leitura inválido',
        }
    segundos = max(0, int((datetime.now() - dt).total_seconds()))
    ok = segundos <= HEARTBEAT_MAX_AGE_SEC
    if ok:
        mensagem = f'Fluxo ativo — última leitura há {segundos} s'
    else:
        mensagem = f'Sem dados recentes ({segundos} s) — cabo, porta ou serial_reader'
    return {
        'ok': ok,
        'ultima': str(raw),
        'segundos': segundos,
        'mensagem': mensagem,
    }


# rota GET / (painel principal)
@app.route('/')
def index():
    leituras = listar_leituras(40)

    formato = request.args.get('formato')

    if formato == 'json':
        return jsonify([dict(l) for l in leituras])

    heartbeat = compute_serial_heartbeat(leituras)
    chart_data = None
    if leituras:
        ordered = list(reversed(leituras))
        chart_data = {
            'labels': [str(row['timestamp']) for row in ordered],
            'temps': [float(row['temperatura']) for row in ordered],
            'umids': [float(row['umidade']) for row in ordered],
        }
    return render_template(
        'index.html',
        leituras=leituras,
        heartbeat=heartbeat,
        chart_data=chart_data,
    )

# rota GET /leitura
@app.route('/leituras')
def listar():
    leituras = listar_leituras()

    formato = request.args.get('formato')

    if formato == 'json':
        return jsonify([dict(l) for l in leituras])

    return render_template('historico.html', leituras=leituras)

# rota POST /leituras (rota do arduino)
@app.route('/leituras', methods=['POST'])
def criar():
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    id_novo = inserir_leitura(
        dados['temperatura'],
        dados['umidade']
    )

    return jsonify({'id': id_novo, 'status': 'criado'}), 201

# GET /leituras/<id>
@app.route('/leituras/<int:id>')
def detalhe(id):
    leitura = buscar_leitura(id)

    if leitura is None:
        return jsonify({'erro': 'Não encontrado'}), 404

    formato = request.args.get('formato')

    if formato == 'json':
        return jsonify(dict(leitura))

    return render_template('editar.html', leitura=leitura)

# PUT /leituras/<id>
@app.route('/leituras/<int:id>', methods=['PUT'])
def atualizar(id):
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    atualizar_leitura(id, dados)

    return jsonify({'status': 'atualizado'})

# DELETE /leituras/<id>
@app.route('/leituras/<int:id>', methods=['DELETE'])
def deletar(id):
    deletar_leitura(id)

    return jsonify({'status': 'deletado'})

# GET /api/estatisticas
@app.route('/api/estatisticas')
def estatisticas():
    conn = get_db_connection()

    stats = conn.execute(
        '''
        SELECT 
            AVG(temperatura) as media_temp,
            MIN(temperatura) as min_temp,
            MAX(temperatura) as max_temp,
            AVG(umidade) as media_umid,
            MIN(umidade) as min_umid,
            MAX(umidade) as max_umid
        FROM leituras
        '''
    ).fetchone()

    conn.close()

    return jsonify(dict(stats))


@app.route('/api/heartbeat')
def api_heartbeat():
    ultimas = listar_leituras(1)
    return jsonify(compute_serial_heartbeat(ultimas))


# pra rodar o servidor
if __name__ == '__main__':
    app.run(debug=False, host=FLASK_BIND_HOST, port=FLASK_PORT)
