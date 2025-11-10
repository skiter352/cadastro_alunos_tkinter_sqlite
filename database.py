import sqlite3
from pathlib import Path

DB_PATH = Path("dados")
DB_FILE = DB_PATH / "banco.db"

def conectar():
    DB_PATH.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    # garantir foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.executescript("""
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
        professor TEXT
    );

    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL NOT NULL,
        matricula TEXT NOT NULL,
        disciplina_id INTEGER NOT NULL,
        FOREIGN KEY(matricula) REFERENCES alunos(matricula) ON DELETE CASCADE,
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso")
