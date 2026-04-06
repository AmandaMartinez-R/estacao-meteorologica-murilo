from flask import Flask, request, jsonify, render_template
from database import *

app = Flask(__name__)

# inicializa banco ao subir o servidor
init_db()

# rota GET / (painel principal)
@app.route('/')
def index():
    leituras = listar_leituras(10)

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
