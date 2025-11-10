import tkinter as tk
from tkinter import ttk, messagebox
from database import criar_tabelas
from alunos import AlunosFrame
from disciplinas import DisciplinasFrame
from notas import NotasFrame
from exportar_json import exportar_dados

def criar_ui():
    root = tk.Tk()
    root.title("Sistema de Cadastro de Alunos")
    root.geometry("800x600")

    style = ttk.Style(root)

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exportar JSON", command=lambda: on_export(root))
    filemenu.add_separator()
    filemenu.add_command(label="Sair", command=root.destroy)
    menubar.add_cascade(label="Arquivo", menu=filemenu)

    root.config(menu=menubar)

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    alunos_frame = AlunosFrame(notebook)
    disciplinas_frame = DisciplinasFrame(notebook)
    notas_frame = NotasFrame(notebook)

    notebook.add(alunos_frame, text='Alunos')
    notebook.add(disciplinas_frame, text='Disciplinas')
    notebook.add(notas_frame, text='Notas')

    return root

def on_export(root):
    try:
        arquivo = exportar_dados()
        messagebox.showinfo("Exportado", f"Backup salvo em: {arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def main():
    criar_tabelas()
    root = criar_ui()
    root.mainloop()

if __name__ == "__main__":
    main()
