# app/ui/tela_excluir_paciente.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.db import paciente_bd

class TelaExcluirPaciente(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg="#f9f9f9")
        self.controlador = controlador

        tk.Label(self, text="Excluir Paciente", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "nome", "idade", "tipo", "contato", "responsavel"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
        self.tree.pack(pady=10, fill="x")

        tk.Button(self, text="Atualizar Lista", command=self.carregar_pacientes).pack()
        tk.Button(self, text="Excluir Selecionado", command=self.excluir_paciente, bg="#E74C3C", fg="white").pack(pady=5)
        tk.Button(self, text="Voltar", command=lambda: controlador.mostrar_tela("menu_gerenciar")).pack(pady=5)

        self.carregar_pacientes()

    def carregar_pacientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        pacientes = paciente_bd.listar()

        pacientes = [
            (1, "João", 25, "Motora", "99999-0000", "Maria"),
            (2, "Ana", 32, "Visual", "88888-1111", "Carlos")
        ]

        for row in pacientes:
            self.tree.insert("", tk.END, values=row)

        print("[LOG] Pacientes carregados para exclusão")

    def excluir_paciente(self):
        item = self.tree.focus()
        if not item:
            messagebox.showerror("Erro", "Selecione um paciente para excluir!")
            return

        dados = self.tree.item(item)["values"]
        if messagebox.askyesno("Confirmação", f"Deseja excluir {dados[1]}?"):

            if paciente_bd.excluir(dados[0]):
                self.carregar_pacientes()
                messagebox.showinfo("Sucesso", "Paciente excluído!")
            else:
                messagebox.showerror("Erro", "Falha ao excluir paciente!")

            print(f"[LOG] Exclusão de paciente ID={dados[0]}")
            self.carregar_pacientes()
            messagebox.showinfo("Sucesso", "Paciente excluído!")
