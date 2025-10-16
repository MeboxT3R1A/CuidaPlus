import tkinter as tk
from tkinter import ttk

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

        # ---------- SEÇÃO DE ESTATÍSTICAS ----------
        frame_stats = tk.Frame(self.root, bg=self.cor_fundo)
        frame_stats.pack(pady=10)

        estatisticas = [
            ("#e67e22", "Total de Pacientes Ativos", "156"),  # Laranja
            ("#27ae60", "Novos Pacientes (Mês)", "12"),       # Verde
            ("#2980b9", "Consultas Hoje", "8"),               # Azul
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
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

        # ---------- CARREGAR PACIENTES ----------
        self.carregar_pacientes_exemplo()

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

    # ---------- MOCK DE PACIENTES ----------
    def carregar_pacientes_exemplo(self):
        pacientes = [
            {"nome": "João Silva", "idade": 24},
            {"nome": "Maria Souza", "idade": 31},
            {"nome": "Carlos Oliveira", "idade": 29},
            {"nome": "Ana Lima", "idade": 22},
            {"nome": "Lucas Pereira", "idade": 35},
            {"nome": "Joào Silva", "idade": 23},
            {"nome": "Daniel Santos", "idade": 67},
            {"nome": "Eduardo Oliveira", "idade": 43},
            {"nome": "Silvana Lima", "idade": 49},
        ]

        for i, p in enumerate(pacientes):
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

            tk.Label(card, text=p["nome"],
                     font=('Arial', 12, 'bold'), bg="white", fg="#2c3e50").pack(pady=(10, 0))
            tk.Label(card, text=f"Idade: {p['idade']}",
                     font=('Arial', 10), bg="white").pack(pady=(0, 10))

            tk.Button(card, text="Ver Mais",
                      bg="#3498db", fg="white", font=('Arial', 10, 'bold')).pack(ipadx=10, ipady=3)

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
