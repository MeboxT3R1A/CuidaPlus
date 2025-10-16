# app/ui/tela_cadastro_paciente.py
import tkinter as tk
from tkinter import messagebox
from app.db import paciente_bd

class TelaCadastroPaciente:
    def __init__(self):
        self.root = tk.Toplevel()  # ou tk.Tk() se quiser uma janela principal
        self.root.title("Cadastro de Paciente")
        self.root.geometry("500x400")
        self.root.configure(bg="#f9f9f9")

        tk.Label(self.root, text="Cadastro de Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        campos = ["Nome", "Idade", "Tipo de Deficiência", "Contato", "Responsável"]
        self.entradas = {}

        for campo in campos:
            frame = tk.Frame(self.root, bg="#f9f9f9")
            frame.pack(pady=5)
            tk.Label(frame, text=f"{campo}:", width=20, anchor="w", bg="#f9f9f9").pack(side="left")
            entrada = tk.Entry(frame, width=30)
            entrada.pack(side="left")
            self.entradas[campo.lower().replace(" ", "_")] = entrada

        tk.Button(self.root, text="Salvar", command=self.salvar_paciente,
                  bg="#4CAF50", fg="white", width=15).pack(pady=15)

        tk.Button(self.root, text="Fechar", command=self.root.destroy,
                  width=15).pack()

    def salvar_paciente(self):
        dados = {k: v.get() for k, v in self.entradas.items()}

        if not dados["nome"]:
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            return

        if paciente_bd.salvar(dados):
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
            for entrada in self.entradas.values():
                entrada.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar paciente!")
