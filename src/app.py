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