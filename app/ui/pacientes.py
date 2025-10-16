# app/ui/pacientes.py
import tkinter as tk
from tkinter import ttk
from app.db import paciente_bd

class TelaPacientes:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pacientes - Visão Geral")
        self.root.geometry("950x650")       # tamanho fixo
        self.root.resizable(False, False)   # bloqueia redimensionamento
        self.root.configure(bg='#f0f0f0')
        self.fonte = ('Arial', 11)
        self.cor_fundo = '#f0f0f0'

        self.criar_interface()

    def criar_interface(self):
        # ---------- TÍTULO PRINCIPAL ----------
        tk.Label(
            self.root,
            text="Pacientes - Visão Geral",
            font=('Arial', 20, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        ).pack(pady=20)

        # ---------- BOTOES DE GERENCIAMENTO (Cadastrar / Editar / Excluir) ----------
        actions_frame = tk.Frame(self.root, bg=self.cor_fundo)
        actions_frame.pack(pady=5)

        tk.Button(actions_frame, text="Cadastrar Paciente", width=18, height=1,
                  bg="#27ae60", fg="white", font=self.fonte,
                  command=self.abrir_cadastrar).grid(row=0, column=0, padx=8)

        tk.Button(actions_frame, text="Editar Paciente", width=18, height=1,
                  bg="#f39c12", fg="white", font=self.fonte,
                  command=self.abrir_editar).grid(row=0, column=1, padx=8)

        tk.Button(actions_frame, text="Excluir Paciente", width=18, height=1,
                  bg="#e74c3c", fg="white", font=self.fonte,
                  command=self.abrir_excluir).grid(row=0, column=2, padx=8)

        # ---------- SEÇÃO DE ESTATÍSTICAS ----------
        total = paciente_bd.total_pacientes()
        novos = paciente_bd.novos_pacientes()
        consultas = paciente_bd.consultas_hoje()

        print(f"[INFO] Estatísticas carregadas: {total} pacientes, {novos} novos, {consultas} consultas hoje.")

        frame_stats = tk.Frame(self.root, bg=self.cor_fundo)
        frame_stats.pack(pady=10)

        estatisticas = [
            ("#e67e22", "Total de Pacientes Ativos", str(total)),  # Laranja
            ("#27ae60", "Novos Pacientes (Mês)", str(novos)),      # Verde
            ("#2980b9", "Consultas Hoje", str(consultas)),         # Azul
        ]

        for i, (cor, titulo, valor) in enumerate(estatisticas):
            card = tk.Frame(frame_stats, bg=cor, width=220, height=100)
            card.grid(row=0, column=i, padx=20)
            card.pack_propagate(False)

            tk.Label(card, text=titulo, bg=cor, fg="white",
                     font=('Arial', 11, 'bold')).pack(pady=(10, 0))
            tk.Label(card, text=valor, bg=cor, fg="white",
                     font=('Arial', 18, 'bold')).pack(pady=(5, 10))

        # ---------- TÍTULO DA LISTA ----------
        tk.Label(
            self.root,
            text="Lista de Pacientes",
            font=('Arial', 16, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        ).pack(pady=15)

        # ---------- FRAME COM SCROLL ----------
        container = tk.Frame(self.root, bg=self.cor_fundo)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.frame_pacientes = tk.Frame(canvas, bg=self.cor_fundo)

        self.frame_pacientes.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.frame_pacientes, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll com mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows

        # ---------- CARREGAR PACIENTES ----------
        self.carregar_pacientes()

        # ---------- BOTÃO DE VOLTAR ----------
        tk.Button(
            self.root,
            text="Voltar à Tela Principal",
            bg="#34495e",
            fg="white",
            font=('Arial', 11, 'bold'),
            command=self.voltar,
            width=25,
            height=2
        ).pack(pady=20)

    # ---------- CARREGAR PACIENTES ----------
    def carregar_pacientes(self):
        # limpa área
        for w in self.frame_pacientes.winfo_children():
            w.destroy()

        pacientes = paciente_bd.listar_pacientes()
        for i, (nome, data_nasc) in enumerate(pacientes):
            card = tk.Frame(
                self.frame_pacientes,
                bg="white",
                width=250,
                height=120,
                highlightbackground="#bdc3c7",
                highlightthickness=1
            )
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15)
            card.pack_propagate(False)

            tk.Label(card, text=nome,
                    font=('Arial', 12, 'bold'), bg="white", fg="#2c3e50").pack(pady=(10, 0))
            tk.Label(card, text=f"Nascimento: {data_nasc}",
                    font=('Arial', 10), bg="white").pack(pady=(0, 10))

            tk.Button(card, text="Ver Mais",
                    bg="#3498db", fg="white", font=('Arial', 10, 'bold')).pack(ipadx=10, ipady=3)

    # ---------- ABERTURA DAS TELAS DE GERENCIAMENTO ----------
    def abrir_cadastrar(self):
        # ---------------- Ponto abrir_cadastrar ----------------
        # importa só no momento para evitar import circular
        from app.ui.tela_cadastro_paciente import TelaCadastroPaciente
        self.root.destroy()
        TelaCadastroPaciente(self.root, self).executar() if hasattr(TelaCadastroPaciente, "executar") else TelaCadastroPaciente(tk.Tk(), self).mainloop()

    def abrir_editar(self):
        # ---------------- Ponto abrir_editar ----------------
        from app.ui.tela_editar_paciente import TelaEditarPaciente
        self.root.destroy()
        TelaEditarPaciente(self.root, self).executar() if hasattr(TelaEditarPaciente, "executar") else TelaEditarPaciente(tk.Tk(), self).mainloop()

    def abrir_excluir(self):
        # ---------------- Ponto abrir_excluir ----------------
        from app.ui.tela_excluir_paciente import TelaExcluirPaciente
        self.root.destroy()
        TelaExcluirPaciente(self.root, self).executar() if hasattr(TelaExcluirPaciente, "executar") else TelaExcluirPaciente(tk.Tk(), self).mainloop()

    # ---------- VOLTAR ----------
    def voltar(self):
        from app.ui.principal import TelaPrincipal
        self.root.destroy()
        TelaPrincipal().executar()

    def executar(self):
        self.root.mainloop()


# Execução direta (para testes isolados)
if __name__ == "__main__":
    TelaPacientes().executar()
