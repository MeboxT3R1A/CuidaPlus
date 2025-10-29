# app/ui/tela_excluir_paciente.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.db import paciente_bd
from app import auth

class TelaExcluirPaciente(tk.Frame):
    def __init__(self, master):
        self.master = master
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

        # Style do Treeview (leve)
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#f2f2f2", foreground="black", relief="flat")
        style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#ffffff", fieldbackground="#ffffff", relief="flat", borderwidth=0)
        style.map("Treeview", background=[("selected", "#cce5ff")])

        # Treeview (sem coluna id visível)
        self.tree = ttk.Treeview(self.janela, columns=("nome", "idade", "tipo", "contato", "responsavel"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center")
        self.tree.pack(padx=40, pady=10, fill="both", expand=True)

        # botões
        tk.Button(self.janela, text="Atualizar Lista", command=self.carregar_pacientes).pack()
        tk.Button(self.janela, text="Excluir Selecionado", command=self._confirmar_exclusao_com_senha, bg="#E74C3C", fg="white").pack(pady=5)
        tk.Button(self.janela, text="Voltar", command=self.voltar, width=15).pack(pady=(10, 60))

        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)
        self.carregar_pacientes()

    def carregar_pacientes(self):
        # limpa
        for i in self.tree.get_children():
            self.tree.delete(i)

        pacientes = paciente_bd.listar_pacientes()

        for row in pacientes:
            self.tree.insert("", tk.END, values=row)

        self.tree.tag_configure("cinza", background="#f2f2f2")
        self.tree.tag_configure("branco", background="#ffffff")
        print("[LOG] Pacientes carregados para exclusão")

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

        # executa exclusão (iid é string, converte para int)
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
        try:
            self.janela.destroy()
        except Exception:
            pass
        try:
            self.master.deiconify()
        except Exception:
            pass
