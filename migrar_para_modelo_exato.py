# migrar_para_modelo_exato.py
import sqlite3
from pathlib import Path
import shutil
import datetime
import sys

DB = Path("dados/banco.db")
if not DB.exists():
    print("Erro: banco não encontrado em:", DB.resolve())
    sys.exit(1)

# backup com timestamp
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup = DB.parent / f"banco_backup_before_migration_{ts}.db"
shutil.copy2(DB, backup)
print("✅ Backup criado em:", backup)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# desligar temporariamente foreign keys para alterações
cur.execute("PRAGMA foreign_keys = OFF;")

# 1) criar novas tabelas com o esquema exato
cur.executescript("""
-- esquema exato solicitado
CREATE TABLE IF NOT EXISTS alunos_new (
    matricula TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    dt_nascimento TEXT
);

CREATE TABLE IF NOT EXISTS disciplinas_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    turno TEXT,
    sala TEXT,
    professor TEXT
);

CREATE TABLE IF NOT EXISTS notas_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,
    matricula TEXT NOT NULL,
    disciplina_id INTEGER NOT NULL,
    FOREIGN KEY(matricula) REFERENCES alunos_new(matricula) ON DELETE CASCADE,
    FOREIGN KEY(disciplina_id) REFERENCES disciplinas_new(id) ON DELETE CASCADE
);
""")
conn.commit()
print("✅ Tabelas novas criadas (alunos_new, disciplinas_new, notas_new)")

# 2) copiar disciplinas
# tentativa: se existir tabela antiga 'disciplinas' copiamos id e nome; outros campos ficam NULL
try:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='disciplinas'")
    if cur.fetchone():
        cur.execute("SELECT id, nome FROM disciplinas")
        rows = cur.fetchall()
        for r in rows:
            cur.execute("INSERT OR IGNORE INTO disciplinas_new (id, nome) VALUES (?, ?)", (r["id"], r["nome"]))
        conn.commit()
        print(f"✅ Copiadas {len(rows)} linhas para disciplinas_new (campos turno/sala/professor em branco)")
    else:
        print("ℹ️ Tabela antiga 'disciplinas' não encontrada — disciplinas_new ficará vazia")
except Exception as e:
    print("⚠️ Erro ao migrar disciplinas:", e)

# 3) copiar alunos
# caso exista coluna matricula na tabela antiga, usa ela; se não, tentamos criar matrícula baseada no id
try:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alunos'")
    if cur.fetchone():
        # detecta colunas
        cols = [c["name"] for c in cur.execute("PRAGMA table_info(alunos)").fetchall()]
        has_matricula = "matricula" in cols
        rows = cur.execute("SELECT * FROM alunos").fetchall()
        cnt = 0
        for r in rows:
            if has_matricula and r["matricula"]:
                matricula = str(r["matricula"])
            else:
                # gerar matrícula baseada no id (se existir) ou um guid simples
                if "id" in cols and r["id"] is not None:
                    matricula = f"M{r['id']}"
                else:
                    matricula = f"M_auto_{cnt+1}"
            nome = r["nome"] if "nome" in cols else ""
            dt = r.get("dt_nascimento") if "dt_nascimento" in cols else None
            cur.execute("INSERT OR IGNORE INTO alunos_new (matricula, nome, dt_nascimento) VALUES (?, ?, ?)",
                        (matricula, nome, dt))
            cnt += 1
        conn.commit()
        print(f"✅ Copiadas {cnt} linhas para alunos_new (matricula gerada quando necessário)")
    else:
        print("ℹ️ Tabela antiga 'alunos' não encontrada — alunos_new ficará vazia")
except Exception as e:
    print("⚠️ Erro ao migrar alunos:", e)

# 4) copiar notas
# estratégia: buscar notas existentes, mapear aluno_id -> matricula (pela tabela antiga 'alunos' ou alunos_new)
try:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notas'")
    if cur.fetchone():
        notas = cur.execute("SELECT * FROM notas").fetchall()
        migrated = 0
        for n in notas:
            # tentar obter valor (pode ser 'nota' ou 'valor')
            valor = None
            if "nota" in n.keys():
                valor = n["nota"]
            elif "valor" in n.keys():
                valor = n["valor"]
            else:
                # pegar qualquer coluna numérica?
                for k in n.keys():
                    if isinstance(n[k], (int, float)) and k not in ("id","aluno_id","disciplina_id"):
                        valor = n[k]
                        break
            # mapear matrícula: primeiramente procurar coluna 'aluno_id'
            matricula = None
            if "aluno_id" in n.keys() and n["aluno_id"] is not None:
                # procura matricula na tabela antiga alunos (se existir)
                cur.execute("SELECT matricula FROM alunos WHERE id=?", (n["aluno_id"],))
                r = cur.fetchone()
                if r and r["matricula"]:
                    matricula = r["matricula"]
                else:
                    # se não existir, procurar por mapeamento em alunos_new via id -> M{id}
                    matricula = f"M{n['aluno_id']}"
            # se já existe campo 'matricula' na nota antiga:
            if "matricula" in n.keys() and n["matricula"]:
                matricula = n["matricula"]
            # disciplina id: pode ser disciplina_id ou disciplina
            disciplina_id = n["disciplina_id"] if "disciplina_id" in n.keys() else n.get("disciplina")
            # se ainda não temos valor ou matricula, pulamos e logamos
            if valor is None or matricula is None or disciplina_id is None:
                print(f"⚠️ Pulando nota id={n['id']}: dados incompletos (valor={valor}, matricula={matricula}, disciplina_id={disciplina_id})")
                continue
            cur.execute("INSERT INTO notas_new (id, valor, matricula, disciplina_id) VALUES (?, ?, ?, ?)",
                        (n["id"], valor, matricula, disciplina_id))
            migrated += 1
        conn.commit()
        print(f"✅ Migradas {migrated} notas para notas_new")
    else:
        print("ℹ️ Tabela antiga 'notas' não encontrada — notas_new ficará vazia")
except Exception as e:
    print("⚠️ Erro ao migrar notas:", e)

# 5) renomear tabelas (após validação manual, você pode apagar as antigas _old)
try:
    cur.executescript("""
    ALTER TABLE alunos RENAME TO alunos_old;
    ALTER TABLE disciplinas RENAME TO disciplinas_old;
    ALTER TABLE notas RENAME TO notas_old;
    ALTER TABLE alunos_new RENAME TO alunos;
    ALTER TABLE disciplinas_new RENAME TO disciplinas;
    ALTER TABLE notas_new RENAME TO notas;
    """)
    conn.commit()
    print("✅ Tabelas antigas renomeadas com sufixo _old e novas renomeadas para nomes finais.")
except Exception as e:
    print("⚠️ Erro ao renomear tabelas:", e)

# 6) reabilitar foreign keys
cur.execute("PRAGMA foreign_keys = ON;")
conn.commit()
conn.close()

print("Migração concluída. Revise os dados e apague as tabelas *_old apenas quando estiver seguro.")
print("Backup disponível em:", backup)
