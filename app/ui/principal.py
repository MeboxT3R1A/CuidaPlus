# app/ui/principal.py
import tkinter as tk
from app.ui.sobre import TelaSobre
from app.ui.pacientes import TelaPacientes

class TelaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestão da Clínica")
        self.root.geometry("950x650")       # tamanho fixo
        self.root.resizable(False, False)   # bloqueia redimensionamento
        self.root.configure(bg='#f0f0f0')
        self.fonte = ('Arial', 11)
        self.cor_fundo = '#f0f0f0'

        self.frame = tk.Frame(self.root, bg=self.cor_fundo)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.criar_interface()

    def criar_interface(self):
        tk.Label(self.frame, text="Sistema de Gestão da Clínica", font=('Arial', 18, 'bold'), bg=self.cor_fundo).pack(pady=30)

        botoes = [
            ("Pacientes", self.abrir_pacientes),
            ("Sobre o Software", self.abrir_sobre),
            ("Logout", self.logout)
        ]

        for texto, comando in botoes:
            tk.Button(self.frame, text=texto, width=25, height=2, command=comando, font=self.fonte, bg="#4CAF50", fg="white").pack(pady=10)

    def abrir_pacientes(self):
        self.root.destroy()
        TelaPacientes().executar()

    def abrir_sobre(self):
        self.root.destroy()
        TelaSobre().executar()

    def logout(self):
        self.root.destroy()
        from app.ui.login import LoginTela
        LoginTela().executar()

    def executar(self):
        self.root.mainloop()
