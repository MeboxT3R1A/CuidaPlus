# app/ui/tela_editar_paciente.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.ui.tela_popup_editar import EditarPopup
from app.db import paciente_bd
from datetime import datetime

class TelaEditarPaciente(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Editar Paciente")
        self.janela.state("zoomed")
        self.janela.configure(bg="#f9f9f9")
        self.janela.resizable(False, False)

        # Título
        tk.Label(self.janela, text="Editar Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=(10,0))

        # Linha preta abaixo do título (simula separação do header)
        tk.Frame(self.janela, height=2, bg="black").pack(fill="x", padx=40, pady=(0,10))

        # ------------------- ESTILO TREEVIEW -------------------
        style = ttk.Style()
        style.theme_use("clam")  # obrigatório para customizações funcionarem

        # Cabeçalho
        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),
            background="#f2f2f2",
            foreground="black",
            relief="flat"
        )

        # Corpo da tabela
        style.configure(
            "Treeview",
            font=("Arial", 11),
            rowheight=28,
            background="#ffffff",
            fieldbackground="#ffffff",
            relief="flat",
            borderwidth=0
        )
        style.map("Treeview", background=[("selected", "#cce5ff")])

        # ------------------- TREEVIEW -------------------
        # agora com coluna 'nascimento' explícita
        self.tree = ttk.Treeview(
            self.janela,
            columns=("nome", "nascimento", "idade", "tipo", "contato", "responsavel"),
            show="headings"
        )
        headings = {
            "nome": "Nome",
            "nascimento": "Nascimento",
            "idade": "Idade",
            "tipo": "Tipo",
            "contato": "Contato",
            "responsavel": "Responsável"
        }
        for col in self.tree["columns"]:
            self.tree.heading(col, text=headings[col])
            # largura inicial razoável
            if col == "nome":
                self.tree.column(col, anchor="w", width=220)
            elif col == "nascimento":
                self.tree.column(col, anchor="center", width=120)
            elif col == "idade":
                self.tree.column(col, anchor="center", width=80)
            else:
                self.tree.column(col, anchor="center", width=140)

        self.tree.pack(padx=40, pady=10, fill="both", expand=True)

        # ------------------- BOTÕES -------------------
        btn_frame = tk.Frame(self.janela, bg="#f9f9f9")
        btn_frame.pack(pady=(0, 40))
        tk.Button(btn_frame, text="Atualizar Lista",
                  command=self.carregar_pacientes).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Editar Selecionado",
                  command=self.editar_paciente).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="Voltar",
                  command=self.voltar, width=15).grid(row=0, column=2, padx=8)

        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)
        self.carregar_pacientes()

    def _formatar_data_br(self, iso_date):
        """Recebe 'YYYY-MM-DD' -> retorna 'DD/MM/YYYY' ou '' se inválido."""
        if not iso_date:
            return ""
        try:
            dt = datetime.strptime(iso_date, "%Y-%m-%d").date()
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return iso_date  # se já estiver em outro formato, retorna cru

    def carregar_pacientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        pacientes = paciente_bd.listar_pacientes()
        for i, row in enumerate(pacientes):
            # row: (id, nome, dataNascimento, idade, tipoDeficiencia, email, responsavel)
            id_ = row[0]
            nome = row[1]
            nascimento_iso = row[2]
            idade = row[3]
            tipo = row[4]
            contato = row[5]
            responsavel = row[6]

            nascimento_br = self._formatar_data_br(nascimento_iso)

            values = (nome, nascimento_br, idade, tipo, contato, responsavel)
            cor = "cinza" if i % 2 == 0 else "branco"
            self.tree.insert("", tk.END, iid=str(id_), values=values, tags=(cor,))

        # Configura cores alternadas
        self.tree.tag_configure("cinza", background="#f2f2f2")
        self.tree.tag_configure("branco", background="#ffffff")

        print("[LOG] Lista de pacientes carregada")

    def editar_paciente(self):
        item = self.tree.focus()
        if not item:
            messagebox.showerror("Erro", "Selecione um paciente!")
            return

        # item é o iid (id do paciente)
        id_paciente = item
        valores = self.tree.item(item)["values"]
        # valores = [nome, nascimento_br, idade, tipo, contato, responsavel]
        dados_para_popup = [id_paciente] + list(valores)  # pop-up espera id na posição 0
        EditarPopup(self.janela, dados_para_popup, self.carregar_pacientes)

    def voltar(self):
        self.janela.destroy()
        self.master.deiconify()
