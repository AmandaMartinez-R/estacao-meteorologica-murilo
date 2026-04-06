import sqlite3

DB = 'dados.db'
# criação da conexão com o banco de dados e configuração para evitar bloqueios
def get_db_connection():
    conn = sqlite3.connect(DB, timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    conn.row_factory = sqlite3.Row
    return conn


# inicialização do banco de dados, criando a tabela se ela não existir
def init_db():
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

# CRUD
# create
def inserir_leitura(temperatura, umidade):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO leituras (temperatura, umidade) VALUES (?, ?)',
        (temperatura, umidade)
    )

    conn.commit()
    conn.close()

    return cursor.lastrowid