# app/ui/tela_popup_editar.py
import tkinter as tk
from tkinter import messagebox
from app.db import paciente_bd
from datetime import datetime

class EditarPopup(tk.Toplevel):
    def __init__(self, parent, dados, callback):
        """
        dados: lista com [id, nome, nascimento_br, idade, tipo, contato, responsavel]
        callback: função para recarregar a lista após salvar
        """
        super().__init__(parent)
        self.callback = callback
        self.title("Editar Paciente")

        # Campos alinhados com cadastro: Nome, Data de Nascimento, Tipo, Email, Responsavel
        campos = [
            ("Nome", "nome"),
            ("Data de Nascimento", "data_nasc"),  # DD/MM/AAAA exibido
            ("Tipo de Deficiencia", "tipo_de_deficiencia"),
            ("Email", "contato"),
            ("Responsavel", "responsavel")
        ]
        self.entradas = {}
        self.id_paciente = dados[0]

        # dados indices:
        # dados[1] = nome
        # dados[2] = nascimento_br (DD/MM/YYYY)
        # dados[3] = idade (não usado para edição)
        # dados[4] = tipo
        # dados[5] = contato (email)
        # dados[6] = responsavel

        valores_map = {
            "nome": dados[1] if len(dados) > 1 else "",
            "data_nasc": dados[2] if len(dados) > 2 else "",
            "tipo_de_deficiencia": dados[4] if len(dados) > 4 else "",
            "contato": dados[5] if len(dados) > 5 else "",
            "responsavel": dados[6] if len(dados) > 6 else ""
        }

        for i, (label, key) in enumerate(campos):
            tk.Label(self, text=label + ":").grid(row=i, column=0, padx=8, pady=6, sticky="e")
            entrada = tk.Entry(self, width=35)
            entrada.grid(row=i, column=1, padx=8, pady=6)
            entrada.insert(0, valores_map.get(key, ""))
            self.entradas[key] = entrada

        tk.Button(self, text="Salvar Alterações", command=self._on_salvar).grid(row=len(campos)+1, column=0, columnspan=2, pady=12)

    def _parse_data_br_to_iso(self, s):
        """Converte 'DD/MM/YYYY' -> 'YYYY-MM-DD' para armazenar no DB."""
        try:
            dt = datetime.strptime(s, "%d/%m/%Y")
            return dt.date().isoformat()
        except Exception:
            return None

    def _on_salvar(self):
        nome = self.entradas["nome"].get().strip()
        data_nasc_br = self.entradas["data_nasc"].get().strip()
        tipo = self.entradas["tipo_de_deficiencia"].get().strip()
        email = self.entradas["contato"].get().strip()
        responsavel = self.entradas["responsavel"].get().strip() or "Responsável não identificado"

        # === Validação ===
        if not nome:
            messagebox.showerror("Erro", "O campo 'Nome' é obrigatório.")
            return

        # --- Data ---
        if not data_nasc_br:
            messagebox.showerror("Erro", "O campo 'Data de Nascimento' é obrigatório.")
            return

        # valida formato e existência real da data
        try:
            data_nasc = datetime.strptime(data_nasc_br, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA e uma data real (ex: 29/02 só em ano bissexto).")
            return

        # verifica se não é futura
        hoje = datetime.now().date()
        if data_nasc > hoje:
            messagebox.showerror("Erro", "A data de nascimento não pode estar no futuro.")
            return

        # --- Tipo ---
        if not tipo:
            messagebox.showerror("Erro", "O campo 'Tipo de Deficiência' é obrigatório.")
            return

        # --- Email ---
        if not email:
            messagebox.showerror("Erro", "O campo 'E-mail' é obrigatório.")
            return
        import re
        padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao_email, email):
            messagebox.showerror("Erro", "Formato de e-mail inválido. Exemplo válido: nome@dominio.com")
            return


        # === Conversão e validação da data ===
        data_iso = self._parse_data_br_to_iso(data_nasc_br)
        if not data_iso:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        # === Recalcula idade ===
        try:
            data_nasc = datetime.strptime(data_iso, "%Y-%m-%d").date()
            hoje = datetime.now().date()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        except Exception:
            messagebox.showerror("Erro", "Não foi possível calcular a idade a partir da data informada.")
            return

        dados = {
            "nome": nome,
            "data_nasc": data_iso,
            "idade": idade,
            "tipo_de_deficiencia": tipo,
            "contato": email,
            "responsavel": responsavel
        }

        try:
            atualizado = paciente_bd.atualizar(int(self.id_paciente), dados)
            if atualizado:
                messagebox.showinfo("Sucesso", f"Paciente '{nome}' atualizado com sucesso!")
                print(f"[LOG] Paciente ID={self.id_paciente} atualizado: {dados}")
                self.callback()  # recarrega a lista
                self.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao atualizar o paciente no banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao salvar: {e}")
            print(f"[ERRO] Erro ao atualizar paciente: {e}")
