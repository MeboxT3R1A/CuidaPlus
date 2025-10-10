#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Software para Clínica Especializada em Pacientes com Deficiência
Sistema de visualização de informações com navegação entre telas
Desenvolvido com Tkinter para Python
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ClinicaApp:
    """
    Classe principal do aplicativo da clínica
    Gerencia a janela principal e controla a navegação entre telas
    """
    
    def __init__(self):
        """Inicializa o aplicativo criando a janela principal"""
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("Clínica Especializada em Pacientes com Deficiência")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configurações de acessibilidade
        self.fonte_grande = ('Arial', 12, 'bold')
        self.fonte_normal = ('Arial', 10)
        self.cor_fundo = '#f0f0f0'
        self.cor_botao = '#4CAF50'
        self.cor_botao_hover = '#45a049'
        
        # Frame principal que conterá todas as telas
        self.main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variável para controlar a tela atual
        self.tela_atual = None
        
        # Inicializa mostrando a tela de login
        self.mostrar_tela_login()
        
    def limpar_tela(self):
        """Remove todos os widgets do frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def criar_botao_nav(self, parent, texto, comando, cor=None):
        """
        Cria botões de navegação com estilo consistente
        """
        if cor is None:
            cor = self.cor_botao
            
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            font=self.fonte_normal,
            bg=cor,
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            borderwidth=2
        )
        return btn
    
    def mostrar_tela_login(self):
        """Exibe a tela de login"""
        self.limpar_tela()
        self.tela_atual = "login"
        
        # Título da aplicação
        titulo = tk.Label(
            self.main_frame,
            text="Clínica Especializada em Pacientes com Deficiência",
            font=('Arial', 16, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        titulo.pack(pady=30)
        
        # Frame para o formulário de login
        login_frame = tk.Frame(self.main_frame, bg=self.cor_fundo)
        login_frame.pack(pady=50)
        
        # Campo de usuário
        lbl_usuario = tk.Label(
            login_frame,
            text="Usuário:",
            font=self.fonte_grande,
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        lbl_usuario.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.entry_usuario = tk.Entry(
            login_frame,
            font=self.fonte_normal,
            width=20
        )
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)
        
        # Campo de senha
        lbl_senha = tk.Label(
            login_frame,
            text="Senha:",
            font=self.fonte_grande,
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        lbl_senha.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.entry_senha = tk.Entry(
            login_frame,
            font=self.fonte_normal,
            width=20,
            show='*'
        )
        self.entry_senha.grid(row=1, column=1, padx=10, pady=10)
        
        # Botão de entrar
        btn_entrar = self.criar_botao_nav(
            login_frame,
            "Entrar",
            self.validar_login
        )
        btn_entrar.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Botão para ir para "Sobre"
        btn_sobre = self.criar_botao_nav(
            self.main_frame,
            "Sobre o Software",
            self.mostrar_tela_sobre,
            '#3498db'
        )
        btn_sobre.pack(pady=10)
    
    def validar_login(self):
        """
        Simula validação de login e vai para a tela principal
        Em um sistema real, aqui seria feita a validação com banco de dados
        """
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        # Simulação simples - aceita qualquer usuário/senha
        if usuario and senha:
            self.mostrar_tela_principal()
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha usuário e senha!")
    
    def mostrar_tela_principal(self):
        """Exibe a tela principal com opções de navegação"""
        self.limpar_tela()
        self.tela_atual = "principal"
        
        # Título
        titulo = tk.Label(
            self.main_frame,
            text="Sistema de Gestão da Clínica",
            font=('Arial', 18, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        titulo.pack(pady=30)
        
        # Frame para os botões de navegação
        nav_frame = tk.Frame(self.main_frame, bg=self.cor_fundo)
        nav_frame.pack(pady=50)
        
        # Botões para as telas de pacientes
        btn_pacientes_geral = self.criar_botao_nav(
            nav_frame,
            "Pacientes - Visão Geral",
            self.mostrar_pacientes_geral
        )
        btn_pacientes_geral.grid(row=0, column=0, padx=10, pady=10)
        
        btn_pacientes_detalhes = self.criar_botao_nav(
            nav_frame,
            "Pacientes - Detalhes",
            self.mostrar_pacientes_detalhes
        )
        btn_pacientes_detalhes.grid(row=0, column=1, padx=10, pady=10)
        
        btn_pacientes_contatos = self.criar_botao_nav(
            nav_frame,
            "Pacientes - Contatos",
            self.mostrar_pacientes_contatos
        )
        btn_pacientes_contatos.grid(row=0, column=2, padx=10, pady=10)
        
        # Botões de navegação geral
        btn_sobre = self.criar_botao_nav(
            self.main_frame,
            "Sobre o Software",
            self.mostrar_tela_sobre,
            '#3498db'
        )
        btn_sobre.pack(pady=10)
        
        btn_logout = self.criar_botao_nav(
            self.main_frame,
            "Logout",
            self.mostrar_tela_login,
            '#e74c3c'
        )
        btn_logout.pack(pady=5)
    
    def mostrar_tela_sobre(self):
        """Exibe a tela 'Sobre o Software'"""
        self.limpar_tela()
        self.tela_atual = "sobre"
        
        # Título
        titulo = tk.Label(
            self.main_frame,
            text="Sobre o Software",
            font=('Arial', 18, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        titulo.pack(pady=30)
        
        # Frame para o conteúdo
        sobre_frame = tk.Frame(self.main_frame, bg=self.cor_fundo)
        sobre_frame.pack(pady=20, padx=50)
        
        # Descrição do software
        descricao = tk.Label(
            sobre_frame,
            text="""
Este sistema foi desenvolvido especificamente para uma clínica especializada 
no atendimento de pacientes com deficiência.

CARACTERÍSTICAS:
• Interface acessível com fontes grandes e alto contraste
• Navegação simplificada entre diferentes seções
• Visualização de informações de pacientes de forma organizada
• Sistema focado na experiência do usuário com necessidades especiais

MISSÃO:
Proporcionar uma ferramenta de gestão eficiente e acessível que facilite 
o atendimento e acompanhamento de pacientes com deficiência, garantindo 
que todos os profissionais da clínica possam utilizar o sistema de forma 
confortável e produtiva.
            """,
            font=self.fonte_normal,
            bg=self.cor_fundo,
            fg='#2c3e50',
            justify=tk.LEFT
        )
        descricao.pack(pady=20)
        
        # Botões de navegação
        btn_voltar = self.criar_botao_nav(
            self.main_frame,
            "Voltar",
            self.mostrar_tela_principal,
            '#3498db'
        )
        btn_voltar.pack(pady=10)
    
    def mostrar_pacientes_geral(self):
        """Exibe a tela 'Pacientes - Visão Geral'"""
        self.limpar_tela()
        self.tela_atual = "pacientes_geral"
        
        # Título
        titulo = tk.Label(
            self.main_frame,
            text="Pacientes - Visão Geral",
            font=('Arial', 18, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        titulo.pack(pady=20)
        
        # Frame para os dados simulados
        dados_frame = tk.Frame(self.main_frame, bg=self.cor_fundo)
        dados_frame.pack(pady=20, padx=50)
        
        # Dados simulados dos pacientes
        dados_pacientes = [
            ("Total de Pacientes Ativos:", "156"),
            ("Novos Pacientes (Este Mês):", "12"),
            ("Consultas Agendadas (Hoje):", "8"),
            ("Pacientes em Acompanhamento:", "134"),
            ("Tipos de Deficiência Mais Comuns:", "Motora (45%), Visual (30%), Auditiva (25%)"),
            ("Taxa de Frequência:", "92%"),
            ("Próxima Consulta:", "João Silva - 14:30")
        ]
        
        # Exibe os dados
        for i, (label, valor) in enumerate(dados_pacientes):
            lbl_titulo = tk.Label(
                dados_frame,
                text=label,
                font=self.fonte_grande,
                bg=self.cor_fundo,
                fg='#2c3e50'
            )
            lbl_titulo.grid(row=i, column=0, sticky='w', padx=10, pady=5)
            
            lbl_valor = tk.Label(
                dados_frame,
                text=valor,
                font=self.fonte_normal,
                bg=self.cor_fundo,
                fg='#27ae60'
            )
            lbl_valor.grid(row=i, column=1, sticky='w', padx=20, pady=5)
        
        # Botões de navegação
        self.criar_botoes_navegacao()
    
    def mostrar_pacientes_detalhes(self):
        """Exibe a tela 'Pacientes - Detalhes'"""
        self.limpar_tela()
        self.tela_atual = "pacientes_detalhes"
        
        # Título
        titulo = tk.Label(
            self.main_frame,
            text="Pacientes - Detalhes",
            font=('Arial', 18, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        titulo.pack(pady=20)
        
        # Frame para os dados simulados
        dados_frame = tk.Frame(self.main_frame, bg=self.cor_fundo)
        dados_frame.pack(pady=20, padx=50)
        
        # Dados simulados detalhados dos pacientes
        pacientes_detalhes = [
            ("Maria Santos", "Deficiência Visual", "Há 2 anos", "Dr. João", "Quinzenal"),
            ("Pedro Oliveira", "Deficiência Motora", "Há 6 meses", "Dra. Ana", "Semanal"),
            ("Ana Costa", "Deficiência Auditiva", "Há 1 ano", "Dr. Carlos", "Mensal"),
            ("Lucas Ferreira", "Deficiência Múltipla", "Há 3 anos", "Dra. Maria", "Semanal"),
            ("Carla Mendes", "Deficiência Intelectual", "Há 8 meses", "Dr. Roberto", "Quinzenal")
        ]
        
        # Cabeçalho da tabela
        headers = ["Nome", "Tipo de Deficiência", "Tempo de Atendimento", "Profissional", "Frequência"]
        for j, header in enumerate(headers):
            lbl_header = tk.Label(
                dados_frame,
                text=header,
                font=self.fonte_grande,
                bg='#34495e',
                fg='white',
                padx=10,
                pady=5
            )
            lbl_header.grid(row=0, column=j, padx=2, pady=2)
        
        # Dados dos pacientes
        for i, paciente in enumerate(pacientes_detalhes, 1):
            for j, dado in enumerate(paciente):
                cor_fundo = '#ecf0f1' if i % 2 == 0 else '#ffffff'
                lbl_dado = tk.Label(
                    dados_frame,
                    text=dado,
                    font=self.fonte_normal,
                    bg=cor_fundo,
                    fg='#2c3e50',
                    padx=10,
                    pady=5
                )
                lbl_dado.grid(row=i, column=j, padx=2, pady=2)
        
        # Botões de navegação
        self.criar_botoes_navegacao()
    
    def mostrar_pacientes_contatos(self):
        """Exibe a tela 'Pacientes - Contatos'"""
        self.limpar_tela()
        self.tela_atual = "pacientes_contatos"
        
        # Título
        titulo = tk.Label(
            self.main_frame,
            text="Pacientes - Contatos",
            font=('Arial', 18, 'bold'),
            bg=self.cor_fundo,
            fg='#2c3e50'
        )
        titulo.pack(pady=20)
        
        # Frame para os dados simulados
        dados_frame = tk.Frame(self.main_frame, bg=self.cor_fundo)
        dados_frame.pack(pady=20, padx=50)
        
        # Dados simulados de contatos dos pacientes
        contatos_pacientes = [
            ("Maria Santos", "(11) 99999-1111", "maria.santos@email.com", "Responsável: José Santos"),
            ("Pedro Oliveira", "(11) 98888-2222", "pedro.oliveira@email.com", "Responsável: Maria Oliveira"),
            ("Ana Costa", "(11) 97777-3333", "ana.costa@email.com", "Responsável: João Costa"),
            ("Lucas Ferreira", "(11) 96666-4444", "lucas.ferreira@email.com", "Responsável: Carla Ferreira"),
            ("Carla Mendes", "(11) 95555-5555", "carla.mendes@email.com", "Responsável: Roberto Mendes")
        ]
        
        # Cabeçalho da tabela
        headers = ["Nome do Paciente", "Telefone", "E-mail", "Informações Adicionais"]
        for j, header in enumerate(headers):
            lbl_header = tk.Label(
                dados_frame,
                text=header,
                font=self.fonte_grande,
                bg='#3498db',
                fg='white',
                padx=10,
                pady=5
            )
            lbl_header.grid(row=0, column=j, padx=2, pady=2)
        
        # Dados dos contatos
        for i, contato in enumerate(contatos_pacientes, 1):
            for j, dado in enumerate(contato):
                cor_fundo = '#e8f4fd' if i % 2 == 0 else '#ffffff'
                lbl_dado = tk.Label(
                    dados_frame,
                    text=dado,
                    font=self.fonte_normal,
                    bg=cor_fundo,
                    fg='#2c3e50',
                    padx=10,
                    pady=5
                )
                lbl_dado.grid(row=i, column=j, padx=2, pady=2)
        
        # Botões de navegação
        self.criar_botoes_navegacao()
    
    def criar_botoes_navegacao(self):
        """
        Cria botões de navegação padrão para todas as telas de pacientes
        """
        nav_frame = tk.Frame(self.main_frame, bg=self.cor_fundo)
        nav_frame.pack(pady=20)
        
        # Botões para outras telas de pacientes
        btn_geral = self.criar_botao_nav(
            nav_frame,
            "Visão Geral",
            self.mostrar_pacientes_geral,
            '#27ae60'
        )
        btn_geral.grid(row=0, column=0, padx=5)
        
        btn_detalhes = self.criar_botao_nav(
            nav_frame,
            "Detalhes",
            self.mostrar_pacientes_detalhes,
            '#f39c12'
        )
        btn_detalhes.grid(row=0, column=1, padx=5)
        
        btn_contatos = self.criar_botao_nav(
            nav_frame,
            "Contatos",
            self.mostrar_pacientes_contatos,
            '#3498db'
        )
        btn_contatos.grid(row=0, column=2, padx=5)
        
        # Botões de navegação geral
        btn_principal = self.criar_botao_nav(
            self.main_frame,
            "Tela Principal",
            self.mostrar_tela_principal,
            '#9b59b6'
        )
        btn_principal.pack(pady=10)
        
        btn_sobre = self.criar_botao_nav(
            self.main_frame,
            "Sobre o Software",
            self.mostrar_tela_sobre,
            '#3498db'
        )
        btn_sobre.pack(pady=5)
        
        btn_logout = self.criar_botao_nav(
            self.main_frame,
            "Logout",
            self.mostrar_tela_login,
            '#e74c3c'
        )
        btn_logout.pack(pady=5)
    
    def executar(self):
        """Inicia o loop principal do aplicativo"""
        self.root.mainloop()

def main():
    """
    Função principal que inicializa e executa o aplicativo
    """
    print("Iniciando aplicativo da Clínica Especializada...")
    app = ClinicaApp()
    app.executar()

if __name__ == "__main__":
    main()
