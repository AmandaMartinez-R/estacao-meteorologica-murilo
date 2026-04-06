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

# read
def listar_leituras(limite=50):
    conn = get_db_connection()

    leituras = conn.execute(
        '''
        SELECT * FROM leituras
        ORDER BY timestamp DESC
        LIMIT ?
        ''',
        (limite,)
    ).fetchall()

    conn.close()
    return leituras

# buscar 
def buscar_leitura(id):
    conn = get_db_connection()

    leitura = conn.execute(
        'SELECT * FROM leituras WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()
    return leitura

#update
def atualizar_leitura(id, dados):
    conn = get_db_connection()

    conn.execute(
        '''
        UPDATE leituras
        SET temperatura = ?, umidade = ?
        WHERE id = ?
        ''',
        (
            dados.get('temperatura'),
            dados.get('umidade'),
            id
        )
    )

    conn.commit()
    conn.close()

# delete
def deletar_leitura(id):
    conn = get_db_connection()

    conn.execute(
        'DELETE FROM leituras WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()