import tkinter as tk

class TelaPacientes:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pacientes - Visão Geral")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        self.fonte = ('Arial', 11)
        self.cor_fundo = '#f0f0f0'

        self.criar_interface()

    def criar_interface(self):
        tk.Label(self.root, text="Pacientes - Visão Geral", font=('Arial', 18, 'bold'), bg=self.cor_fundo, fg='#2c3e50').pack(pady=20)

        dados = [
            ("Total de Pacientes Ativos:", "156"),
            ("Novos Pacientes (Este Mês):", "12"),
            ("Consultas Agendadas (Hoje):", "8")
        ]

        frame = tk.Frame(self.root, bg=self.cor_fundo)
        frame.pack(pady=10)

        for i, (titulo, valor) in enumerate(dados):
            tk.Label(frame, text=titulo, font=('Arial', 12, 'bold'), bg=self.cor_fundo).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            tk.Label(frame, text=valor, font=('Arial', 12), bg=self.cor_fundo, fg="#27ae60").grid(row=i, column=1, sticky='w', padx=10, pady=5)

        tk.Button(self.root, text="Voltar à Tela Principal", bg="#3498db", fg="white", command=self.voltar, width=25, height=2).pack(pady=20)

    def voltar(self):
        from ui.principal import TelaPrincipal
        self.root.destroy()
        TelaPrincipal().executar()


    def executar(self):
        self.root.mainloop()
