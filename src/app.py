from flask import Flask, request, jsonify, render_template
from database import *

app = Flask(__name__)

# inicializa banco ao subir o servidor
init_db()