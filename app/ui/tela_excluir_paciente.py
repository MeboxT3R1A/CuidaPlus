# app/ui/tela_excluir_paciente.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.db import paciente_bd
from app import auth
from datetime import datetime

class TelaExcluirPaciente(tk.Frame):
    def __init__(self, master, on_success=None):
        self.master = master
        self.on_success = on_success
        self.master.withdraw()
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Excluir Paciente")
        self.janela.state("zoomed")
        self.janela.configure(bg="#f9f9f9")
        self.janela.resizable(False, False)

        # Título + linha preta (igual ao editar)
        tk.Label(self.janela, text="Excluir Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=(10,0))
        tk.Frame(self.janela, height=2, bg="black").pack(fill="x", padx=40, pady=(0,10))

        # ------------------- ESTILO TREEVIEW (mesmo do editar) -------------------
        style = ttk.Style()
        style.theme_use("clam")  # usar mesmo tema do editar para consistência

        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),
            background="#f2f2f2",
            foreground="black",
            relief="flat"
        )
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
        # agora com coluna 'nascimento' explícita para manter paridade com editar
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
            if col == "nome":
                self.tree.column(col, anchor="w", width=220)
            elif col == "nascimento":
                self.tree.column(col, anchor="center", width=120)
            elif col == "idade":
                self.tree.column(col, anchor="center", width=80)
            else:
                self.tree.column(col, anchor="center", width=140)

        self.tree.pack(padx=40, pady=10, fill="both", expand=True)

        # ------------------- BOTÕES (alinhados horizontalmente, igual editar) -------------------
        btn_frame = tk.Frame(self.janela, bg="#f9f9f9")
        btn_frame.pack(pady=(0, 40))
        tk.Button(btn_frame, text="Atualizar Lista",
                  command=self.carregar_pacientes).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Excluir Selecionado",
                  command=self._confirmar_exclusao_com_senha, bg="#E74C3C", fg="white").grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="Voltar", command=self.voltar, width=15).grid(row=0, column=2, padx=8)

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
            return iso_date

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

    def _confirmar_exclusao_com_senha(self):
        item = self.tree.focus()
        if not item:
            messagebox.showerror("Erro", "Selecione um paciente para excluir!")
            return

        dados = self.tree.item(item)["values"]
        nome = dados[0] if dados else "<desconhecido>"

        current = auth.get_current_user()
        if not current:
            messagebox.showerror("Erro", "Usuário atual não encontrado. Faça login novamente.")
            print("[ERRO] Tentativa de exclusão sem usuário logado.")
            return

        # pede senha (modal)
        senha = simpledialog.askstring("Verificação", f"Digite sua senha ({current.get('nome','usuário')}) para confirmar exclusão de '{nome}':", show='*', parent=self.janela)
        if senha is None:
            return

        try:
            ok = auth.verify_password(current.get("id"), senha)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar senha: {e}")
            print(f"[ERRO] Falha ao verificar senha: {e}")
            return

        if not ok:
            messagebox.showerror("Erro", "Senha incorreta. Exclusão abortada.")
            print("[ERRO] Tentativa de exclusão com senha incorreta.")
            return

        # confirmação final
        if not messagebox.askyesno("Confirmação", f"Deseja realmente excluir {nome}? (autenticado)"):
            return

        try:
            id_paciente = int(self.tree.focus())
        except Exception:
            messagebox.showerror("Erro", "ID inválido do paciente.")
            print("[ERRO] IID inválido:", self.tree.focus())
            return

        try:
            paciente_bd.excluir(id_paciente)
            self.carregar_pacientes()
            messagebox.showinfo("Sucesso", "Paciente excluído!")
            print(f"[LOG] Paciente ID={id_paciente} excluído com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir paciente: {e}")
            print(f"[ERRO] Falha ao excluir paciente ID={id_paciente}: {e}")

    def excluir_paciente(self):
        # mantido por compatibilidade
        self._confirmar_exclusao_com_senha()

    def voltar(self):
        # Primeiro: preferir chamar o callback on_success se fornecido
        try:
            if callable(self.on_success):
                self.on_success()
            else:
                # fallback antigo: tenta atualizar a master caso esta possua o método
                if hasattr(self.master, "carregar_pacientes"):
                    self.master.carregar_pacientes()
        except Exception as e:
            print(f"[ERRO ao atualizar lista ao voltar]: {e}")
        
        self.janela.destroy()
        try:
            self.master.deiconify()
        except Exception:
            pass

