import sqlite3
import json
from pathlib import Path
from database import conectar

OUT = Path("dados") / "backup.json"

def exportar_dados():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, matricula FROM alunos")
    alunos = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT id, nome, codigo FROM disciplinas")
    disciplinas = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT id, aluno_id, disciplina_id, nota FROM notas")
    notas = [dict(r) for r in cur.fetchall()]
    conn.close()

    data = {
        "alunos": alunos,
        "disciplinas": disciplinas,
        "notas": notas
    }
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return OUT

if __name__ == "__main__":
    arquivo = exportar_dados()
    print(f"Backup salvo em: {arquivo}")
