# app/ui/app_controller.py
import tkinter as tk
from app.ui.tela_pacientes import TelaPacientes
from app.ui.tela_cadastro_paciente import TelaCadastroPaciente
from app.ui.tela_editar_paciente import TelaEditarPaciente
from app.ui.tela_excluir_paciente import TelaExcluirPaciente

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cuida+")
        self.geometry("950x650")
        self.configure(bg="#f0f0f0")
        self.frames = {}

        # Inicializa todas as telas
        for F in (TelaPacientes, TelaCadastroPaciente, TelaEditarPaciente, TelaExcluirPaciente):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(TelaPacientes)

    def show_frame(self, tela):
        frame = self.frames[tela]
        frame.tkraise()
