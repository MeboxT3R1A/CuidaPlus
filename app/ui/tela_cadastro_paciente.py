# app/ui/tela_cadastro_paciente.py
import tkinter as tk
from tkinter import messagebox, ttk
import re
from datetime import datetime, date
from app.db import paciente_bd

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class TelaCadastroPaciente:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Cadastro de Paciente")
        self.janela.geometry("520x400")
        self.janela.configure(bg="#f9f9f9")
        self.janela.resizable(False, False)

        tk.Label(self.janela, text="Cadastro de Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)


        # campos
        campos = [
            ("Nome", "nome"),
            ("Data de Nascimento", "data_nasc"),
            ("Tipo de Deficiência", "tipo_deficiencia"),
        ]
        self.entradas = {}

        for label_text, key in campos:
            frame = tk.Frame(self.janela, bg="#f9f9f9")
            frame.pack(pady=6, padx=12, fill="x")
            tk.Label(frame, text=f"{label_text}:", width=28, anchor="w", bg="#f9f9f9").pack(side="left")
            entry = tk.Entry(frame, width=28)
            entry.pack(side="left")
            self.entradas[key] = entry

        # liga automação na data
        self.entradas["data_nasc"].insert(0, "DD/MM/AAAA")  # placeholder inicial
        self.entradas["data_nasc"].config(fg="gray")
        self.entradas["data_nasc"].bind("<FocusIn>", self._clear_placeholder)
        self.entradas["data_nasc"].bind("<FocusOut>", self._restore_placeholder)
        self.entradas["data_nasc"].bind("<KeyRelease>", self._formatar_data_event)

        # contato: tipo + campo
        frame_contato = tk.Frame(self.janela, bg="#f9f9f9")
        frame_contato.pack(pady=6, padx=12, fill="x")
        tk.Label(frame_contato, text="Tipo de Contato:", width=28, anchor="w", bg="#f9f9f9").pack(side="left")

        self.contato_tipo = ttk.Combobox(frame_contato, values=["Telefone", "Email"], state="readonly", width=26)
        self.contato_tipo.current(0)
        self.contato_tipo.pack(side="left")
        self.contato_tipo.bind("<<ComboboxSelected>>", self._on_tipo_contato_change)

        frame_contato2 = tk.Frame(self.janela, bg="#f9f9f9")
        frame_contato2.pack(pady=6, padx=12, fill="x")
        tk.Label(frame_contato2, text="Contato:", width=28, anchor="w", bg="#f9f9f9").pack(side="left")
        self.contato_entry = tk.Entry(frame_contato2, width=28)
        self.contato_entry.pack(side="left")

        # bind para formatação telefone
        self.contato_entry.bind("<KeyRelease>", self._formatar_contato_event)

        # botões
        tk.Button(self.janela, text="Salvar", command=self.salvar_paciente,
                  bg="#4CAF50", fg="white", width=15).pack(pady=15)

        tk.Button(self.janela, text="Voltar", command=self.voltar,
                  width=15).pack()

        # Quando a janela for fechada manualmente, voltar também
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)


    # ---------------- formatação e validações ----------------
    # métodos
    def _clear_placeholder(self, event):
        e = event.widget
        if e.get() == "DD/MM/AAAA":
            e.delete(0, tk.END)
            e.config(fg="black")

    def _restore_placeholder(self, event):
        e = event.widget
        if not e.get():
            e.insert(0, "DD/MM/AAAA")
            e.config(fg="gray")

    def _formatar_data_event(self, event=None):
        e = self.entradas["data_nasc"]
        s = e.get()
        
        # ignora placeholder
        if s == "DD/MM/AAAA":
            return

        # salva posição do cursor
        pos = e.index(tk.INSERT)

        digits = re.sub(r"[^\d]", "", s)[:8]  # só números
        new_text = ""
        for i, d in enumerate(digits):
            new_text += d
            if i == 1 or i == 3:
                if len(digits) > i + 1:  # só coloca / se houver próximo dígito
                    new_text += "/"

        # atualiza Entry somente se mudou
        if new_text != s:
            e.delete(0, tk.END)
            e.insert(0, new_text)
            # tenta restaurar posição do cursor
            if pos <= len(new_text):
                e.icursor(pos)
            else:
                e.icursor(len(new_text))



    def _on_tipo_contato_change(self, event=None):
        """Ajusta placeholder/limpeza ao mudar tipo de contato."""
        self.contato_entry.delete(0, tk.END)

    def _formatar_contato_event(self, event=None):
        """Formata o campo de contato se for telefone; caso email, deixa como está."""
        tipo = self.contato_tipo.get()
        s = self.contato_entry.get()
        if tipo == "Telefone":
            digits = re.sub(r"[^\d]", "", s)[:11]  # DDD + 8/9 dígitos
            formatted = self._format_telefone_digits(digits)
            self.contato_entry.delete(0, tk.END)
            self.contato_entry.insert(0, formatted)
        # se email, não formatar automaticamente

    def _format_telefone_digits(self, digits: str) -> str:
        if not digits:
            return ""
        if len(digits) <= 2:
            return f"({digits}"
        if len(digits) <= 6:  # (XX) XXXX
            return f"({digits[:2]}) {digits[2:]}"
        if len(digits) <= 10:  # (XX) XXXX-XXXX (8 digits after DDD)
            return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        # 11 digits -> (XX) XXXXX-XXXX
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:11]}"

    def _validar_data(self, s: str):
        """Valida formato DD/MM/YYYY e plausibilidade."""
        try:
            parts = s.split("/")
            if len(parts) != 3:
                return False, "Formato inválido. Use DD/MM/AAAA."
            d, m, y = parts
            if len(y) != 4:
                return False, "Ano inválido. Use 4 dígitos (AAAA)."
            dt = date(int(y), int(m), int(d))  # pode lançar ValueError
            hoje = date.today()
            if dt > hoje:
                return False, "Data de nascimento no futuro."
            idade = hoje.year - dt.year - ((hoje.month, hoje.day) < (dt.month, dt.day))
            if idade < 0 or idade > 120:
                return False, "Idade inválida (idade > 120 ou negativa)."
            return True, dt
        except ValueError:
            return False, "Data inválida."

    def _validar_contato(self, tipo, valor):
        if tipo == "Telefone":
            digits = re.sub(r"[^\d]", "", valor)
            if len(digits) not in (10, 11):
                return False, "Telefone deve ter DDD + 8 ou 9 dígitos."
            return True, self._format_telefone_digits(digits)
        else:  # Email
            if not EMAIL_RE.match(valor):
                return False, "Email inválido."
            return True, valor.strip()



    # ---------------- salvar ----------------
    def salvar_paciente(self):
        nome = self.entradas["nome"].get().strip()
        data_raw = self.entradas["data_nasc"].get().strip()
        tipo_def = self.entradas["tipo_deficiencia"].get().strip()
        contato_tipo = self.contato_tipo.get()
        contato_raw = self.contato_entry.get().strip()

        # validações básicas
        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            return

        ok_date, date_info = self._validar_data(data_raw)
        if not ok_date:
            messagebox.showerror("Erro - Data", date_info)
            return
        # date_info é um objeto date
        data_iso = date_info.isoformat()  # YYYY-MM-DD

        ok_cont, cont_info = self._validar_contato(contato_tipo, contato_raw)
        if not ok_cont:
            messagebox.showerror("Erro - Contato", cont_info)
            return
        contato_formatado = cont_info

        dados = {
            "nome": nome,
            "data_nasc": data_iso,
            "tipo_deficiencia": tipo_def,
            "contato_tipo": contato_tipo,
            "contato": contato_formatado
        }

        try:
            saved = paciente_bd.salvar(dados)
            if saved:
                messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
                # limpa campos
                for entrada in self.entradas.values():
                    entrada.delete(0, tk.END)
                self.contato_entry.delete(0, tk.END)
                self.contato_tipo.current(0)
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar paciente!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

    # ---------------- voltar ----------------

    def voltar(self):
        try:
            self.janela.destroy()
        except Exception:
            pass
        try:
            self.master.deiconify()  # Mostra de novo a tela de pacientes
        except Exception:
            pass
