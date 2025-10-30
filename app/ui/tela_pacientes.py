# app/ui/tela_pacientes.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
from app.db import paciente_bd
from app.ui.tela_ver_mais import TelaVerMais

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

    # ---------- UTIL ----------    
    def _calcular_idade(self, data_str):
        """
        Aceita 'YYYY-MM-DD' (preferencial) ou 'DD/MM/YYYY'.
        Retorna idade em anos (int) ou None se inválido.
        """
        if not data_str:
            return None
        try:
            if "-" in data_str:
                dt = datetime.strptime(data_str, "%Y-%m-%d").date()
            elif "/" in data_str:
                dt = datetime.strptime(data_str, "%d/%m/%Y").date()
            else:
                # formato inesperado
                return None
            hoje = date.today()
            idade = hoje.year - dt.year - ((hoje.month, hoje.day) < (dt.month, dt.day))
            return idade
        except Exception as e:
            print(f"[ERRO] _calcular_idade: formato inválido '{data_str}': {e}")
            return None

    # ---------- CARREGAR PACIENTES ----------
    def carregar_pacientes(self):
        # limpa área
        for w in self.frame_pacientes.winfo_children():
            w.destroy()

        pacientes = paciente_bd.listar()
        for i, (id_paciente, nome, data_nasc) in enumerate(pacientes):
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

            # calcula idade e mostra em anos
            idade = self._calcular_idade(data_nasc)
            if idade is None:
                idade_text = "Idade desconhecida"
            elif idade == 1:
                idade_text = "1 ano"
            else:
                idade_text = f"{idade} anos"

            tk.Label(card, text=f"Idade: {idade_text}",
                    font=('Arial', 10), bg="white").pack(pady=(0, 10))

            tk.Button(
                card,
                text="Ver Mais",
                bg="#3498db",
                fg="white",
                font=('Arial', 10, 'bold'),
                command=lambda pid=id_paciente: self.abrir_ver_mais(pid)
            ).pack(ipadx=10, ipady=3)

    def abrir_ver_mais(self, id_paciente):
        TelaVerMais(id_paciente).executar()

    
    def abrir_cadastrar(self):
        from app.ui.tela_cadastro_paciente import TelaCadastroPaciente
        self.root.withdraw()
        TelaCadastroPaciente(self.root, on_success=self._atualizar_lista)

    def abrir_editar(self):
        from app.ui.tela_editar_paciente import TelaEditarPaciente
        self.root.withdraw()
        TelaEditarPaciente(self.root, on_success=self._atualizar_lista)

    def abrir_excluir(self):
        from app.ui.tela_excluir_paciente import TelaExcluirPaciente
        self.root.withdraw()
        TelaExcluirPaciente(self.root, on_success=self._atualizar_lista)

    def _atualizar_lista(self):
        self.carregar_pacientes()
        self.root.deiconify()

    # ---------- VOLTAR ----------
    def voltar(self):
        from app.ui.tela_principal import TelaPrincipal
        self.root.destroy()
        TelaPrincipal().executar()

    def executar(self):
        self.root.mainloop()


# Execução direta (para testes isolados)
if __name__ == "__main__":
    TelaPacientes().executar()
