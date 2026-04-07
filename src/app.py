from flask import Flask, request, jsonify, render_template
from database import *

app = Flask(__name__)

# inicializa banco ao subir o servidor
init_db()

# rota GET / (painel principal)
@app.route('/')
def index():
    leituras = listar_leituras(40)

    formato = request.args.get('formato')

    if formato == 'json':
        return jsonify([dict(l) for l in leituras])

    return render_template('index.html', leituras=leituras)

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

# pra rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
