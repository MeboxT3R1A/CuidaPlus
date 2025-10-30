# app/ui/tela_cadastro_paciente.py
import tkinter as tk
from tkinter import messagebox
import re
from datetime import date
from app.db import paciente_bd

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class TelaCadastroPaciente:
    def __init__(self, master, on_success=None):
        self.master = master
        self.on_success = on_success      
        self.master.withdraw()
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Cadastro de Paciente")
        self.janela.geometry("350x300")
        self.janela.configure(bg="#f9f9f9")
        self.janela.resizable(False, False)

        tk.Label(self.janela, text="Cadastro de Paciente",
                 font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        # campos
        campos = [
            ("Nome", "nome"),
            ("Data de Nascimento", "data_nasc"),
            ("Tipo de Deficiência", "tipo_deficiencia"),
            ("Email", "email"),
            ("Responsável", "responsavel")
        ]
        self.entradas = {}

        for label_text, key in campos:
            # Campo especial para data
            if key == "data_nasc":
                frame = tk.Frame(self.janela, bg="#f9f9f9")
                frame.pack(pady=6, padx=12, fill="x")
                tk.Label(frame, text="Data de nascimento:", width=20, anchor="w", bg="#f9f9f9").pack(side="left")

                sub = tk.Frame(frame, bg="#f9f9f9")
                sub.pack(side="left")

                self.data_parts = {}
                partes = [("dia", 4, "DD"), ("mes", 4, "MM"), ("ano", 6, "AAAA")]

                for i, (chave, width, placeholder) in enumerate(partes):
                    e = tk.Entry(sub, width=width, justify="center", fg="gray")
                    e.insert(0, placeholder)
                    e.bind("<FocusIn>", lambda ev, ph=placeholder, ent=e: self._clear_placeholder_parte(ev, ph))
                    e.bind("<FocusOut>", lambda ev, ph=placeholder, ent=e: self._restore_placeholder_parte(ev, ph))
                    e.bind("<KeyRelease>", lambda ev, w=width: self._limitar_digitos(ev, w))
                    e.pack(side="left")
                    self.data_parts[chave] = e

                    if i < 2:
                        tk.Label(sub, text="/", bg="#f9f9f9").pack(side="left")

                self.entradas[key] = self.data_parts
                continue

            # Campos normais
            frame = tk.Frame(self.janela, bg="#f9f9f9")
            frame.pack(pady=6, padx=12, fill="x")
            tk.Label(frame, text=f"{label_text}:", width=20, anchor="w", bg="#f9f9f9").pack(side="left")
            entry = tk.Entry(frame, width=28)
            entry.pack(side="left")
            self.entradas[key] = entry

        # botões
        tk.Button(self.janela, text="Salvar", command=self.salvar_paciente,
                  bg="#4CAF50", fg="white", width=15).pack(pady=15)

        tk.Button(self.janela, text="Voltar", command=self.voltar,
                  width=15).pack()

        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)

    # ---------------- formatação e validações ----------------
    def _clear_placeholder_parte(self, event, placeholder):
        e = event.widget
        if e.get() == placeholder:
            e.delete(0, tk.END)
            e.config(fg="black")

    def _restore_placeholder_parte(self, event, placeholder):
        e = event.widget
        if not e.get():
            e.insert(0, placeholder)
            e.config(fg="gray")

    def _limitar_digitos(self, event, limite):
        e = event.widget
        texto = re.sub(r"[^\d]", "", e.get())
        if len(texto) > limite:
            texto = texto[:limite]
        e.delete(0, tk.END)
        e.insert(0, texto)
        
    def _obter_data_nascimento(self):
        partes = self.entradas["data_nasc"]
        dia = partes["dia"].get()
        mes = partes["mes"].get()
        ano = partes["ano"].get()
        if any(p in ("DD", "MM", "AAAA", "") for p in [dia, mes, ano]):
            return None
        return f"{dia.zfill(2)}/{mes.zfill(2)}/{ano.zfill(4)}"

    def _validar_data(self, s: str):
        try:
            d, m, y = s.split("/")
            if len(y) != 4:
                return False, "Ano inválido. Use 4 dígitos (AAAA)."
            dt = date(int(y), int(m), int(d))
            hoje = date.today()
            if dt > hoje:
                return False, "Data de nascimento no futuro."
            idade = hoje.year - dt.year - ((hoje.month, hoje.day) < (dt.month, dt.day))
            if idade < 0 or idade > 120:
                return False, "Idade inválida (idade > 120 ou negativa)."
            return True, dt
        except Exception:
            return False, "Data inválida."

    def _validar_email(self, valor):
        valor = valor.strip()
        if not EMAIL_RE.match(valor):
            return False, "Email inválido."
        return True, valor

    # ---------------- salvar ----------------
    def salvar_paciente(self):
        nome = self.entradas["nome"].get().strip()
        data_raw = self._obter_data_nascimento()
        tipo_def = self.entradas["tipo_deficiencia"].get().strip()
        email_raw = self.entradas["email"].get().strip()
        responsavel = self.entradas["responsavel"].get().strip() or "Responsavel não identificado"

        # === Validação de campos obrigatórios ===
        if not nome or not data_raw or not tipo_def or not email_raw:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios (exceto Responsável).")
            print("[ERRO] Campos obrigatórios vazios.")
            return

        # === Validação de data ===
        ok_date, date_info = self._validar_data(data_raw)
        if not ok_date:
            messagebox.showerror("Erro na Data", date_info)
            print(f"[ERRO] {date_info}")
            return
        data_iso = date_info.isoformat()

        # === Validação de e-mail ===
        ok_email, email_valido = self._validar_email(email_raw)
        if not ok_email:
            messagebox.showerror("Erro no E-mail", email_valido)
            print(f"[ERRO] {email_valido}")
            return

        if not responsavel:
            responsavel = "Responsável não identificado"

        dados = {
            "nome": nome,
            "data_nasc": data_iso,
            "tipo_deficiencia": tipo_def,
            "contato": email_valido,
            "responsavel": responsavel,
        }

        # === Inserção no banco ===
        try:
            saved = paciente_bd.salvar(dados)
            if saved:
                messagebox.showinfo("Sucesso", f"Paciente '{nome}' cadastrado com sucesso!")
                if self.on_success:
                    self.on_success()
                self.voltar()
            else:
                messagebox.showerror("Erro", "Falha ao salvar paciente no banco de dados.")
                print("[ERRO] Falha ao cadastrar paciente.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao salvar: {e}")
            print(f"[ERRO] Erro ao salvar no banco: {e}")


    # ---------------- voltar ----------------
    def voltar(self):
        # Tenta primeiro avisar o callback (se houver) — faz isso antes de destruir a janela.
        try:
            if callable(self.on_success):
                try:
                    self.on_success()
                except Exception as e:
                    print(f"[ERRO] on_success() levantou exceção: {e}")
        except Exception as e:
            print(f"[ERRO] ao verificar on_success: {e}")

        # Fecha a janela do cadastro e revela a janela principal (root) de forma segura.
        try:
            self.janela.destroy()
        except Exception:
            pass
        try:
            self.master.deiconify()
        except Exception:
            pass

