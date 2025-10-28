# app/ui/tela_excluir_paciente.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.db import paciente_bd

class TelaExcluirPaciente(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Excluir Paciente")
        self.janela.state("zoomed")
        self.janela.configure(bg="#f9f9f9")
        self.janela.resizable(False, False)

        # ------------------- TÍTULO -------------------
        tk.Label(self.janela, text="Excluir Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        # ------------------- ESTILO TREEVIEW -------------------
        style = ttk.Style()
        style.theme_use("clam")

        # Cabeçalho
        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),
            background="#f2f2f2",
            foreground="black",
            relief="flat"
        )

        # Linha preta abaixo do cabeçalho
        style.layout("Treeview.Heading", [
            ("Treeheading.cell", {'sticky': 'nswe'}),
            ("Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Treeheading.text", {'sticky': 'we'})
                ]})
            ], 'border': '1'})  # aqui adiciona a borda inferior preta
        ])

        # Corpo da tabela
        style.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            rowheight=28,
            relief="flat"
        )
        style.map("Treeview", background=[("selected", "#cce5ff")])
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        # ------------------- TREEVIEW -------------------
        self.tree = ttk.Treeview(
            self.janela,
            columns=("nome", "idade", "tipo", "contato", "responsavel"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=40, pady=10, fill="both", expand=True)

        # ------------------- BOTÕES -------------------
        tk.Button(self.janela, text="Atualizar Lista",
                  command=self.carregar_pacientes).pack()
        tk.Button(self.janela, text="Excluir Selecionado",
                  command=self.excluir_paciente, bg="#E74C3C", fg="white").pack(pady=5)
        tk.Button(self.janela, text="Voltar",
                  command=self.voltar, width=15).pack(pady=(10, 60))

        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)

        self.carregar_pacientes()

    def carregar_pacientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        pacientes = paciente_bd.listar()
        for i, row in enumerate(pacientes):
            cor = "cinza" if i % 2 == 0 else "branco"
            self.tree.insert("", tk.END, values=row[1:], tags=(cor,))
        
        self.tree.tag_configure("cinza", background="#f2f2f2")
        self.tree.tag_configure("branco", background="#ffffff")

        print("[LOG] Pacientes carregados para exclusão")

    def excluir_paciente(self):
        item = self.tree.focus()
        if not item:
            messagebox.showerror("Erro", "Selecione um paciente para excluir!")
            return

        dados = self.tree.item(item)["values"]
        id_ = paciente_bd.listar()[self.tree.index(item)][0]  # pega ID real
        if messagebox.askyesno("Confirmação", f"Deseja excluir {dados[0]}?"):
            try:
                paciente_bd.excluir(id_)
                self.carregar_pacientes()
                messagebox.showinfo("Sucesso", "Paciente excluído!")
                print(f"[LOG] Paciente ID={id_} excluído com sucesso")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir paciente: {e}")

    def voltar(self):
        self.janela.destroy()
        self.master.deiconify()
