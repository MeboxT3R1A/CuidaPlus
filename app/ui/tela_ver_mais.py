import tkinter as tk
from tkinter import ttk
from app.db.paciente_bd import obter_detalhes_paciente

class TelaVerMais:
    def __init__(self, id_paciente):
        self.id_paciente = id_paciente
        self.root = tk.Tk()
        self.root.title("Detalhes do Paciente")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f6f7")

        self.dados = obter_detalhes_paciente(id_paciente)
        self.montar_interface()

    def montar_interface(self):
        if not self.dados:
            tk.Label(self.root, text="Paciente não encontrado.", font=("Arial", 14, "bold"), fg="red", bg="#f4f6f7").pack(pady=20)
            return

        frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        tk.Label(frame, text=f"Detalhes do Paciente", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        conteudo = tk.Frame(frame, bg="white")
        conteudo.pack(pady=10)

        def linha(label, valor):
            tk.Label(conteudo, text=f"{label}:", anchor="w", width=20, bg="white", font=("Arial", 10, "bold")).pack()
            tk.Label(conteudo, text=str(valor or "—"), anchor="w", bg="white", font=("Arial", 10)).pack(pady=(0, 10))

        linha("Nome", self.dados["nome"])
        linha("Email", self.dados["email"])
        linha("Data de Nascimento", self.dados["dataNascimento"])
        linha("Idade", self.dados["idade"])
        linha("Tipo de Deficiência", self.dados["tipoDeficiencia"])
        linha("Responsável", self.dados["responsavel"])
        linha("Peso", self.dados["peso"])
        linha("Altura", self.dados["altura"])
        linha("Biografia", self.dados["biografia"])
        linha("Outras Observações", self.dados["outras_observacoes"])
        linha("Último Atendimento", self.dados["ultima_data"])
        linha("Observações Atendimento", self.dados["ultima_obs"])
        linha("Diagnóstico", self.dados["diagnostico"])

        tk.Button(frame, text="Fechar", bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                  command=self.root.destroy, width=12).pack(pady=15)

    def executar(self):
        self.root.mainloop()
