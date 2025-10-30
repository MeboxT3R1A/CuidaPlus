# CuidaPlus

Sistema desenvolvido como **Projeto Integrador** para gestão de pacientes com deficiência em uma clínica.  
Permite o cadastro, edição e acompanhamento de pacientes, com controle de atendimentos, diagnósticos, relatórios e usuários administrativos.

---

## 🧩 Tecnologias Utilizadas
- **Python 3.13+**
- **Tkinter** — Interface gráfica
- **SQLite3** — Banco de dados local
- **PyInstaller** — Empacotamento para executável
- **Hashlib** — Criptografia de senha

---

## 📂 Estrutura do Projeto
CuidaPlus/
│
├── app/
│ ├── db/
│ │ ├── connection.py # Conexão com o banco SQLite
│ │ └── setup.py # Criação e população inicial do banco
│ │
│ ├── ui/
│ │ ├── telas principais e formulários em Tkinter
│ │ └── ...
│ │
│ ├── main.py # Ponto de entrada da aplicação
│ └── utils.py # Funções auxiliares (se houver)
│
├── Executavel/
│ ├── build/ # Arquivos temporários da build
│ ├── dist/ # Executável gerado (.exe)
│ └── spec/ # Arquivo .spec do PyInstaller
│
├── CuidaPlusIcon.ico # Ícone do aplicativo
├── requirements.txt # Dependências (opcional)
└── README.md

---

## 🚀 Execução

### Rodando via Python
```bash
python app/main.py
