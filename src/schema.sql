CREATE TABLE IF NOT EXISTS leituras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL NOT NULL,
    umidade REAL NOT NULL,
    localizacao TEXT DEFAULT 'São Paulo',
    timestamp DATETIME DEFAULT (datetime('now','localtime'))
);