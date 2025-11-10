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

        frm_inputs.columnconfigure(1, weight=1)

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill='x', pady=6)

        ttk.Button(frm_buttons, text="Incluir", command=self.incluir).pack(side='left')
        ttk.Button(frm_buttons, text="Alterar", command=self.alterar).pack(side='left', padx=5)
        ttk.Button(frm_buttons, text="Excluir", command=self.excluir).pack(side='left')
        ttk.Button(frm_buttons, text="Listar", command=self.listar).pack(side='left', padx=5)

        cols = ("id", "nome", "matricula")
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor='center')
        self.tree.pack(fill='both', expand=True, pady=6)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event=None):
        sel = self.tree.focus()
        if sel:
            vals = self.tree.item(sel, 'values')
            self.nome.delete(0, 'end')
            self.nome.insert(0, vals[1])
            self.matricula.delete(0, 'end')
            self.matricula.insert(0, vals[2])

    def incluir(self):
        n = self.nome.get().strip()
        m = self.matricula.get().strip()
        if not validar_texto(n, m):
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO alunos (nome, matricula) VALUES (?, ?)", (n, m))
            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno incluído")
            self.limpar_campos()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def listar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, matricula FROM alunos ORDER BY nome")
        for r in cur.fetchall():
            self.tree.insert('', 'end', values=(r['id'], r['nome'], r['matricula']))
        conn.close()

    def alterar(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um aluno")
            return
        vals = self.tree.item(sel, 'values')
        aluno_id = vals[0]
        n = self.nome.get().strip()
        m = self.matricula.get().strip()
        if not validar_texto(n, m):
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE alunos SET nome=?, matricula=? WHERE id=?", (n, m, aluno_id))
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
        aluno_id = vals[0]
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
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
