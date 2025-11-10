from tkinter import messagebox

def validar_texto(*vals):
    return all(v and str(v).strip() for v in vals)

def confirmar_exclusao(entidade="item"):
    return messagebox.askyesno("Confirmar", f"Deseja realmente excluir este {entidade}?")
