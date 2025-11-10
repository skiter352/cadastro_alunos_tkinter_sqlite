import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from utils import validar_texto, confirmar_exclusao

class AlunosFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.criar_widgets()
        self.listar()

    def criar_widgets(self):
        frm_inputs = ttk.Frame(self)
        frm_inputs.pack(fill='x')

        ttk.Label(frm_inputs, text="Nome:").grid(row=0, column=0, sticky='w')
        self.nome = ttk.Entry(frm_inputs)
        self.nome.grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Label(frm_inputs, text="Matrícula:").grid(row=1, column=0, sticky='w')
        self.matricula = ttk.Entry(frm_inputs)
        self.matricula.grid(row=1, column=1, sticky='ew', padx=5)

        ttk.Label(frm_inputs, text="Data Nasc (YYYY-MM-DD):").grid(row=2, column=0, sticky='w')
        self.dt = ttk.Entry(frm_inputs)
        self.dt.grid(row=2, column=1, sticky='ew', padx=5)

        frm_inputs.columnconfigure(1, weight=1)

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill='x', pady=6)

        ttk.Button(frm_buttons, text="Incluir", command=self.incluir).pack(side='left')
        ttk.Button(frm_buttons, text="Alterar", command=self.alterar).pack(side='left', padx=5)
        ttk.Button(frm_buttons, text="Excluir", command=self.excluir).pack(side='left')
        ttk.Button(frm_buttons, text="Listar", command=self.listar).pack(side='left', padx=5)

        cols = ("matricula", "nome", "dt_nascimento")
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=10)
        self.tree.heading("matricula", text="Matrícula")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("dt_nascimento", text="Dt Nasc")
        self.tree.column("matricula", width=120, anchor='center')
        self.tree.column("nome", anchor='w')
        self.tree.column("dt_nascimento", width=110, anchor='center')
        self.tree.pack(fill='both', expand=True, pady=6)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event=None):
        sel = self.tree.focus()
        if sel:
            vals = self.tree.item(sel, 'values')
            self.matricula.delete(0, 'end'); self.matricula.insert(0, vals[0])
            self.nome.delete(0, 'end'); self.nome.insert(0, vals[1])
            self.dt.delete(0, 'end'); self.dt.insert(0, vals[2] if vals[2] is not None else "")

    def incluir(self):
        n = self.nome.get().strip()
        m = self.matricula.get().strip()
        dt = self.dt.get().strip() or None
        if not validar_texto(n, m):
            messagebox.showwarning("Atenção", "Preencha nome e matrícula")
            return
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO alunos (matricula, nome, dt_nascimento) VALUES (?, ?, ?)", (m, n, dt))
            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno incluído")
            self.limpar_campos()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def listar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT matricula, nome, dt_nascimento FROM alunos ORDER BY nome")
        for r in cur.fetchall():
            self.tree.insert('', 'end', values=(r['matricula'], r['nome'], r['dt_nascimento']))
        conn.close()

    def alterar(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um aluno")
            return
        vals = self.tree.item(sel, 'values')
        old_matricula = vals[0]
        m = self.matricula.get().strip()
        n = self.nome.get().strip()
        dt = self.dt.get().strip() or None
        if not validar_texto(n, m):
            messagebox.showwarning("Atenção", "Preencha nome e matrícula")
            return
        conn = conectar()
        cur = conn.cursor()
        try:
            # Se matrícula foi alterada, precisamos atualizar a PK (SQLite permite UPDATE PK)
            cur.execute("UPDATE alunos SET matricula=?, nome=?, dt_nascimento=? WHERE matricula=?", (m, n, dt, old_matricula))
            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno alterado")
            self.limpar_campos()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def excluir(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um aluno")
            return
        if not confirmar_exclusao("aluno"):
            return
        vals = self.tree.item(sel, 'values')
        matricula = vals[0]
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM alunos WHERE matricula=?", (matricula,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno excluído")
            self.limpar_campos()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def limpar_campos(self):
        self.nome.delete(0, 'end')
        self.matricula.delete(0, 'end')
        self.dt.delete(0, 'end')
