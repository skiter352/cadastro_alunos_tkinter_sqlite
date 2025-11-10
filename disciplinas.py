import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from utils import validar_texto, confirmar_exclusao

class DisciplinasFrame(ttk.Frame):
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

        ttk.Label(frm_inputs, text="Turno:").grid(row=1, column=0, sticky='w')
        self.turno = ttk.Entry(frm_inputs)
        self.turno.grid(row=1, column=1, sticky='ew', padx=5)

        ttk.Label(frm_inputs, text="Sala:").grid(row=2, column=0, sticky='w')
        self.sala = ttk.Entry(frm_inputs)
        self.sala.grid(row=2, column=1, sticky='ew', padx=5)

        ttk.Label(frm_inputs, text="Professor:").grid(row=3, column=0, sticky='w')
        self.professor = ttk.Entry(frm_inputs)
        self.professor.grid(row=3, column=1, sticky='ew', padx=5)

        frm_inputs.columnconfigure(1, weight=1)

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill='x', pady=6)

        ttk.Button(frm_buttons, text="Incluir", command=self.incluir).pack(side='left')
        ttk.Button(frm_buttons, text="Alterar", command=self.alterar).pack(side='left', padx=5)
        ttk.Button(frm_buttons, text="Excluir", command=self.excluir).pack(side='left')
        ttk.Button(frm_buttons, text="Listar", command=self.listar).pack(side='left', padx=5)

        cols = ("id", "nome", "turno", "sala", "professor")
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor='center' if c=="id" else 'w')
        self.tree.pack(fill='both', expand=True, pady=6)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event=None):
        sel = self.tree.focus()
        if sel:
            vals = self.tree.item(sel, 'values')
            self.nome.delete(0, 'end'); self.nome.insert(0, vals[1])
            self.turno.delete(0, 'end'); self.turno.insert(0, vals[2] or "")
            self.sala.delete(0, 'end'); self.sala.insert(0, vals[3] or "")
            self.professor.delete(0, 'end'); self.professor.insert(0, vals[4] or "")

    def incluir(self):
        n = self.nome.get().strip()
        turno = self.turno.get().strip() or None
        sala = self.sala.get().strip() or None
        prof = self.professor.get().strip() or None
        if not validar_texto(n):
            messagebox.showwarning("Atenção", "Preencha o nome")
            return
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO disciplinas (nome, turno, sala, professor) VALUES (?, ?, ?, ?)", (n, turno, sala, prof))
            conn.commit()
            messagebox.showinfo("Sucesso", "Disciplina incluída")
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
        cur.execute("SELECT id, nome, turno, sala, professor FROM disciplinas ORDER BY nome")
        for r in cur.fetchall():
            self.tree.insert('', 'end', values=(r['id'], r['nome'], r['turno'], r['sala'], r['professor']))
        conn.close()

    def alterar(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma disciplina")
            return
        vals = self.tree.item(sel, 'values')
        disc_id = vals[0]
        n = self.nome.get().strip()
        turno = self.turno.get().strip() or None
        sala = self.sala.get().strip() or None
        prof = self.professor.get().strip() or None
        if not validar_texto(n):
            messagebox.showwarning("Atenção", "Preencha o nome")
            return
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE disciplinas SET nome=?, turno=?, sala=?, professor=? WHERE id=?", (n, turno, sala, prof, disc_id))
            conn.commit()
            messagebox.showinfo("Sucesso", "Disciplina alterada")
            self.limpar_campos()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def excluir(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma disciplina")
            return
        if not confirmar_exclusao("disciplina"):
            return
        vals = self.tree.item(sel, 'values')
        disc_id = vals[0]
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM disciplinas WHERE id=?", (disc_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Disciplina excluída")
            self.limpar_campos()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def limpar_campos(self):
        self.nome.delete(0, 'end')
        self.turno.delete(0, 'end')
        self.sala.delete(0, 'end')
        self.professor.delete(0, 'end')
