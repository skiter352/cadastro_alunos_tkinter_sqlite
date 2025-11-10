import sqlite3
from pathlib import Path

DB_PATH = Path("dados")
DB_FILE = DB_PATH / "banco.db"

def conectar():
    DB_PATH.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            nota REAL NOT NULL,
            FOREIGN KEY(aluno_id) REFERENCES alunos(id),
            FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso")
