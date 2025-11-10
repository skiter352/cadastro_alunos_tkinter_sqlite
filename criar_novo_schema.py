import sqlite3
from pathlib import Path

caminho_banco = "dados/banco.db"

ddl = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS alunos (
    matricula TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    dt_nascimento TEXT
);

CREATE TABLE IF NOT EXISTS disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    turno TEXT,
    sala TEXT,
    professor TEXT,
    codigo TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,
    matricula TEXT NOT NULL,
    disciplina_id INTEGER NOT NULL,
    FOREIGN KEY(matricula) REFERENCES alunos(matricula) ON DELETE CASCADE,
    FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
);
"""

p = Path(caminho_banco)
if not p.exists():
    print(f"Erro: banco não encontrado em: {p.resolve()}")
else:
    conn = sqlite3.connect(caminho_banco)
    try:
        conn.executescript(ddl)
        conn.commit()
        print("✅ Novo esquema criado com sucesso!")
    finally:
        conn.close()
