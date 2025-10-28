# app/ui/login.py
import tkinter as tk
from tkinter import messagebox
from app.ui.principal import TelaPrincipal
from app.db import login_bd
from app import auth

class TelaLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cuida + Mais")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        self.fonte_grande = ('Arial', 12, 'bold')
        self.fonte_normal = ('Arial', 10)
        self.cor_fundo = '#f0f0f0'
        self.cor_botao = '#4CAF50'

        self.frame = tk.Frame(self.root, bg=self.cor_fundo)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.criar_login()

    def criar_login(self):
        titulo_frame = tk.Frame(self.frame, bg=self.cor_fundo)
        titulo_frame.pack(pady=30)

        tk.Label(
            titulo_frame,
            text="Cuida",
            font=('Arial', 32, 'bold'),
            fg="#2ecc71",
            bg=self.cor_fundo
        ).pack(side="left")

        tk.Label(
            titulo_frame,
            text=" + Mais",
            font=('Arial', 32, 'bold'),
            fg="#e74c3c",
            bg=self.cor_fundo
        ).pack(side="left")

        login_frame = tk.Frame(self.frame, bg=self.cor_fundo)
        login_frame.pack(pady=50)

        tk.Label(login_frame, text="E-mail:", font=self.fonte_grande, bg=self.cor_fundo).grid(row=0, column=0, padx=10, pady=10)
        self.entry_usuario = tk.Entry(login_frame, font=self.fonte_normal, width=20)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_frame, text="Senha:", font=self.fonte_grande, bg=self.cor_fundo).grid(row=1, column=0, padx=10, pady=10)
        self.entry_senha = tk.Entry(login_frame, font=self.fonte_normal, width=20, show='*')
        self.entry_senha.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(
            login_frame,
            text="Entrar",
            bg=self.cor_botao,
            fg="white",
            font=self.fonte_normal,
            command=self.validar_login
        ).grid(row=2, column=0, columnspan=2, pady=20, ipadx=40)

    def validar_login(self):
        email = self.entry_usuario.get().strip().lower()  # normalize
        senha = self.entry_senha.get().strip()

        if not email or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        usuario = login_bd.autenticar_usuario(email, senha)

        if usuario:
            # usa a variável correta e registra em log
            auth.set_current_user(usuario)
            print(f"[LOGIN] Usuário logado: {usuario}")  # log no terminal
            messagebox.showinfo("Bem-vindo", f"Olá, {usuario['nome']}!")
            self.root.destroy()
            TelaPrincipal().executar()
        else:
            print(f"[LOGIN] Falha de autenticação para: {email}")
            # limpa campo de senha para evitar reuso
            self.entry_senha.delete(0, tk.END)
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def executar(self):
        self.root.mainloop()
