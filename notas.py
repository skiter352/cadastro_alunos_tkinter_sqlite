import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from utils import validar_texto, confirmar_exclusao

class NotasFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.criar_widgets()
        self.carregar_combo()
        self.listar()

    def criar_widgets(self):
        frm_inputs = ttk.Frame(self)
        frm_inputs.pack(fill='x')

        ttk.Label(frm_inputs, text="Aluno:").grid(row=0, column=0, sticky='w')
        self.aluno_cb = ttk.Combobox(frm_inputs, state='readonly')
        self.aluno_cb.grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Label(frm_inputs, text="Disciplina:").grid(row=1, column=0, sticky='w')
        self.disc_cb = ttk.Combobox(frm_inputs, state='readonly')
        self.disc_cb.grid(row=1, column=1, sticky='ew', padx=5)

        ttk.Label(frm_inputs, text="Nota:").grid(row=2, column=0, sticky='w')
        self.nota_entry = ttk.Entry(frm_inputs)
        self.nota_entry.grid(row=2, column=1, sticky='ew', padx=5)

        frm_inputs.columnconfigure(1, weight=1)

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill='x', pady=6)

        ttk.Button(frm_buttons, text="Incluir", command=self.incluir).pack(side='left')
        ttk.Button(frm_buttons, text="Alterar", command=self.alterar).pack(side='left', padx=5)
        ttk.Button(frm_buttons, text="Excluir", command=self.excluir).pack(side='left')
        ttk.Button(frm_buttons, text="Listar", command=self.listar).pack(side='left', padx=5)

        cols = ("id", "aluno", "disciplina", "nota")
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor='center')
        self.tree.pack(fill='both', expand=True, pady=6)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def carregar_combo(self):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM alunos ORDER BY nome")
        alunos = cur.fetchall()
        cur.execute("SELECT id, nome FROM disciplinas ORDER BY nome")
        disciplinas = cur.fetchall()
        conn.close()

        self.aluno_map = {f"{r['nome']} (id:{r['id']})": r['id'] for r in alunos}
        self.disc_map = {f"{r['nome']} (id:{r['id']})": r['id'] for r in disciplinas}

        self.aluno_cb['values'] = list(self.aluno_map.keys())
        self.disc_cb['values'] = list(self.disc_map.keys())

    def on_select(self, event=None):
        sel = self.tree.focus()
        if sel:
            vals = self.tree.item(sel, 'values')
            # id, aluno, disciplina, nota
            self.nota_entry.delete(0, 'end')
            self.nota_entry.insert(0, vals[3])
            # selecionar combos
            aluno_key = next((k for k,v in self.aluno_map.items() if str(v)==str(vals[1])), None)
            disc_key = next((k for k,v in self.disc_map.items() if str(v)==str(vals[2])), None)
            if aluno_key:
                self.aluno_cb.set(aluno_key)
            if disc_key:
                self.disc_cb.set(disc_key)

    def incluir(self):
        aluno_sel = self.aluno_cb.get()
        disc_sel = self.disc_cb.get()
        nota = self.nota_entry.get().strip()
        if not (aluno_sel and disc_sel and nota):
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return
        try:
            nota_val = float(nota)
        except ValueError:
            messagebox.showwarning("Atenção", "Nota inválida")
            return
        aluno_id = self.aluno_map[aluno_sel]
        disc_id = self.disc_map[disc_sel]
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)", (aluno_id, disc_id, nota_val))
            conn.commit()
            messagebox.showinfo("Sucesso", "Nota incluída")
            self.limpar_campos()
            self.carregar_combo()
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
        cur.execute("SELECT n.id, n.aluno_id, n.disciplina_id, n.nota, a.nome as aluno_nome, d.nome as disc_nome "
                    "FROM notas n "
                    "JOIN alunos a ON a.id = n.aluno_id "
                    "JOIN disciplinas d ON d.id = n.disciplina_id "
                    "ORDER BY a.nome")
        for r in cur.fetchall():
            # insert id, aluno_id, disciplina_id, nota (shows ids internally)
            self.tree.insert('', 'end', values=(r['id'], r['aluno_id'], r['disciplina_id'], r['nota']))
        conn.close()

    def alterar(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma nota")
            return
        vals = self.tree.item(sel, 'values')
        nota_id = vals[0]
        aluno_sel = self.aluno_cb.get()
        disc_sel = self.disc_cb.get()
        nota = self.nota_entry.get().strip()
        if not (aluno_sel and disc_sel and nota):
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return
        try:
            nota_val = float(nota)
        except ValueError:
            messagebox.showwarning("Atenção", "Nota inválida")
            return
        aluno_id = self.aluno_map[aluno_sel]
        disc_id = self.disc_map[disc_sel]
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE notas SET aluno_id=?, disciplina_id=?, nota=? WHERE id=?", (aluno_id, disc_id, nota_val, nota_id))
            conn.commit()
            messagebox.showinfo("Sucesso", "Nota alterada")
            self.limpar_campos()
            self.carregar_combo()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def excluir(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma nota")
            return
        if not confirmar_exclusao("nota"):
            return
        vals = self.tree.item(sel, 'values')
        nota_id = vals[0]
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM notas WHERE id=?", (nota_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Nota excluída")
            self.limpar_campos()
            self.carregar_combo()
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

    def limpar_campos(self):
        self.aluno_cb.set("")
        self.disc_cb.set("")
        self.nota_entry.delete(0, 'end')
