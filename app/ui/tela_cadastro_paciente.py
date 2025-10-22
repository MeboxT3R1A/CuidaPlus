import tkinter as tk
from tkinter import messagebox
from app.db import paciente_bd

class TelaCadastroPaciente:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Cadastro de Paciente")
        self.janela.geometry("500x400")
        self.janela.configure(bg="#f9f9f9")

        tk.Label(self.janela, text="Cadastro de Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        campos = ["Nome", "Idade", "Tipo de Deficiência", "Contato", "Responsável"]
        self.entradas = {}

        for campo in campos:
            frame = tk.Frame(self.janela, bg="#f9f9f9")
            frame.pack(pady=5)
            tk.Label(frame, text=f"{campo}:", width=20, anchor="w", bg="#f9f9f9").pack(side="left")
            entrada = tk.Entry(frame, width=30)
            entrada.pack(side="left")
            self.entradas[campo.lower().replace(" ", "_")] = entrada

        tk.Button(self.janela, text="Salvar", command=self.salvar_paciente,
                  bg="#4CAF50", fg="white", width=15).pack(pady=15)

        tk.Button(self.janela, text="Voltar", command=self.voltar,
                  width=15).pack()

        # Quando a janela for fechada manualmente, voltar também
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)

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

    def voltar(self):
        self.janela.destroy()
        self.master.deiconify()  # Mostra de novo a tela de pacientes
