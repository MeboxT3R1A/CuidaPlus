# app/ui/tela_editar_paciente.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.ui.tela_popup_editar import EditarPopup
from app.db import paciente_bd

class TelaEditarPaciente(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg="#f9f9f9")
        self.controlador = controlador

        tk.Label(self, text="Editar Paciente", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "nome", "idade", "tipo", "contato", "responsavel"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
        self.tree.pack(pady=10, fill="x")

        tk.Button(self, text="Atualizar Lista", command=self.carregar_pacientes).pack()
        tk.Button(self, text="Editar Selecionado", command=self.editar_paciente).pack(pady=5)
        tk.Button(self, text="Voltar", command=lambda: controlador.mostrar_tela("menu_gerenciar")).pack(pady=5)

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
        EditarPopup(self, dados, self.carregar_pacientes)
