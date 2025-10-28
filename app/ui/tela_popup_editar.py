# app/ui/tela_popup_editar.py
import tkinter as tk
from tkinter import messagebox
from app.db import paciente_bd

class EditarPopup(tk.Toplevel):
    def __init__(self, parent, dados, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Editar Paciente")

        campos = ["Nome", "Idade", "Tipo de Deficiencia", "Contato", "Responsavel"]
        self.entradas = {}

        for i, campo in enumerate(campos):
            tk.Label(self, text=campo + ":").grid(row=i, column=0, padx=5, pady=3)
            entrada = tk.Entry(self, width=30)
            entrada.grid(row=i, column=1)
            entrada.insert(0, dados[i+1])
            self.entradas[campo.lower().replace(" ", "_")] = entrada

        tk.Button(self, text="Salvar Alterações", command=lambda: self.salvar(dados[0])).grid(row=6, column=0, columnspan=2, pady=10)

    def salvar(self, id_):
        dados = {k: v.get() for k, v in self.entradas.items()}

        if paciente_bd.atualizar(id_, dados):
            messagebox.showinfo("Sucesso", "Paciente atualizado!")
        else:
            messagebox.showerror("Erro", "Falha ao atualizar paciente!")

        print(f"[LOG] Atualização de paciente ID={id_}: {dados}")

        self.callback()
        self.destroy()

