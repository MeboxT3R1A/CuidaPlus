# app/ui/tela_editar_paciente.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.ui.tela_popup_editar import EditarPopup
from app.db import paciente_bd

class TelaEditarPaciente(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Cadastro de Paciente")
        self.janela.geometry("500x400")
        self.janela.configure(bg="#f9f9f9")

        # título
        tk.Label(self.janela, text="Editar Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        # tabela
        self.tree = ttk.Treeview(
            self.janela,
            columns=("id", "nome", "idade", "tipo", "contato", "responsavel"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
        self.tree.pack(pady=10, fill="x")

        # botões
        tk.Button(self.janela, text="Atualizar Lista",
                  command=self.carregar_pacientes).pack()
        tk.Button(self.janela, text="Editar Selecionado",
                  command=self.editar_paciente).pack(pady=5)
        tk.Button(self.janela, text="Voltar",
                  command=self.voltar, width=15).pack(pady=10)
        
                # Quando a janela for fechada manualmente, voltar também
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)
        # carrega dados
        self.carregar_pacientes()

    def carregar_pacientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        pacientes = paciente_bd.listar()
        for row in pacientes:
            self.tree.insert("", tk.END, values=row)

        print("[LOG] Lista de pacientes carregada")

    def editar_paciente(self):
        item = self.tree.focus()
        if not item:
            messagebox.showerror("Erro", "Selecione um paciente!")
            return

        dados = self.tree.item(item)["values"]
        EditarPopup(self.janela, dados, self.carregar_pacientes)

    def voltar(self):
        self.janela.destroy()
        self.master.deiconify()
