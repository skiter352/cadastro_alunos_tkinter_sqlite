# 🧑‍🎓 Sistema de Cadastro de Alunos — Tkinter + SQLite + JSON

Projeto completo em **Python** utilizando **Tkinter** para interface gráfica, **SQLite** como banco de dados local e **JSON** para exportação de backup.  
Desenvolvido como parte da disciplina **Desenvolvimento Rápido em Python**, com foco em CRUD completo (Criar, Listar, Alterar e Excluir).

---

## 🚀 Funcionalidades Principais

✅ **Cadastro de Alunos** — Nome e Matrícula  
✅ **Cadastro de Disciplinas** — Nome e Código  
✅ **Cadastro de Notas** — Associação entre Aluno e Disciplina  
✅ **Exportação de Dados** — Backup automático em formato JSON  
✅ **Interface gráfica (Tkinter)** — Totalmente interativa e funcional  
✅ **Banco de dados persistente (SQLite)**  

---

## 💾 Tecnologias Utilizadas

| Categoria | Tecnologia |
|------------|-------------|
| Linguagem  | Python 3 |
| GUI        | Tkinter |
| Banco de Dados | SQLite3 |
| Arquivo de Backup | JSON |
| Organização | Módulos separados por entidade (Aluno, Disciplina, Nota) |

---

## 🧩 Estrutura do Projeto

```
cadastro_alunos_tkinter_sqlite/
│
├── main.py               # Arquivo principal do sistema
├── database.py           # Conexão e criação das tabelas SQLite
├── alunos.py             # CRUD completo para alunos
├── disciplinas.py        # CRUD completo para disciplinas
├── notas.py              # CRUD completo para notas
├── exportar_json.py      # Exporta todos os dados em JSON
├── utils.py              # Funções auxiliares (validação, confirmações)
│
├── dados/                # Pasta de dados
│   ├── banco.db          # Banco de dados SQLite (gerado em runtime)
│   └── backup.json       # Backup exportado em JSON
│
├── requirements.txt      # Dependências do projeto
├── .gitignore            # Arquivos ignorados no Git
└── README.md             # Este arquivo
```

---

## ⚙️ Como Executar

### 1️⃣ Pré-requisitos
- Python 3.8 ou superior instalado.

### 2️⃣ Instalação
Clone o repositório:
```bash
git clone https://github.com/seuusuario/cadastro_alunos_tkinter_sqlite.git
cd cadastro_alunos_tkinter_sqlite
```

(Opcional) Crie um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

Instale dependências:
```bash
pip install -r requirements.txt
```

### 3️⃣ Execução
```bash
python main.py
```

---

## 🗄️ Banco de Dados

O sistema utiliza **SQLite** para persistência local.  
As tabelas são criadas automaticamente na primeira execução.

**Tabelas:**
- `alunos (id, nome, matricula)`
- `disciplinas (id, nome, codigo)`
- `notas (id, aluno_id, disciplina_id, nota)`

---

## 📤 Exportação para JSON

Os dados podem ser exportados para arquivo JSON pelo menu:
```
Arquivo → Exportar JSON
```

O backup será salvo automaticamente em:
```
dados/backup.json
```

---

## 👨‍💻 Autor

**Nícolas Alessandro**  
Desenvolvido como parte do projeto **Desenvolvimento Rápido em Python** — 2025.

---

## 🧠 Licença

Este projeto é de uso acadêmico e livre para estudo e modificação.
---

## 🗂️ Novidades nesta versão

**Atualizações importantes (migração de esquema)**  
- Banco migrado para novo modelo de dados conforme diagrama:
  - **ALUNO** — `matricula (PK), nome, dt_nascimento`
  - **DISCIPLINA** — `id (PK autoinc), nome, turno, sala, professor`
  - **NOTA** — `id (PK autoinc), valor, matricula (FK), disciplina_id (FK)`
- Mantivemos backup automático antes da migração: `dados/banco_backup_before_migration_YYYYMMDD_HHMMSS.db`
- Tabelas antigas renomeadas como `*_old` após migração (ex: `alunos_old`) — disponíveis para verificação.

**Arquivos novos adicionados**
- `migrar_para_modelo_exato.py` — script de migração (faz backup automático e recria as tabelas no formato solicitado).
- `criar_novo_schema.py` — script para criar o DDL do novo esquema (sem migração de dados).
- Atualizações em: `database.py`, `alunos.py`, `disciplinas.py`, `notas.py` — agora usam `matricula` como chave primária do aluno e suportam os novos campos.

---

## 🧭 Como rodar (atualizado)

1. Clone (ou baixe o ZIP):
```bash
git clone https://github.com/skiter352/cadastro_alunos_tkinter_sqlite.git
cd cadastro_alunos_tkinter_sqlite
