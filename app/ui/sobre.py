import tkinter as tk

class TelaSobre:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sobre o Software")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        self.cor_fundo = '#f0f0f0'
        self.criar_interface()

    def criar_interface(self):
        tk.Label(
            self.root,
            text="Sobre o Software",
            font=('Arial', 18, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        ).pack(pady=30)

        descricao = tk.Label(
            self.root,
            text=(
                "Este sistema foi desenvolvido especificamente para uma clínica especializada "
                "no atendimento de pacientes com deficiência.\n\n"
                "CARACTERÍSTICAS:\n"
                "• Interface acessível e simples\n"
                "• Navegação intuitiva\n"
                "• Foco em acessibilidade e eficiência\n\n"
                "MISSÃO:\n"
                "Promover uma gestão humanizada e tecnológica no acompanhamento de pessoas com deficiência, "
                "oferecendo uma plataforma acessível, intuitiva e eficiente que otimize o trabalho dos profissionais "
                "e melhore a experiência de cada paciente."
            ),
            bg=self.cor_fundo,
            font=('Arial', 11),
            justify="left",
            wraplength=650,  # 👈 quebra automática (~650px de largura)
            fg='#2c3e50'
        )
        descricao.pack(padx=40, pady=20)

        # Botão Voltar
        tk.Button(
            self.root,
            text="Voltar",
            bg="#3498db",
            fg="white",
            font=('Arial', 11, 'bold'),
            width=15,
            height=2,
            command=self.voltar
        ).pack(pady=25)


    def voltar(self):
        from ui.principal import TelaPrincipal
        self.root.destroy()
        TelaPrincipal().executar()


    def executar(self):
        self.root.mainloop()
