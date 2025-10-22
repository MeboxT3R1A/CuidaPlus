# app/main.py
import os
import sys

# Garante que o diretório raiz do projeto esteja no path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from app.ui.tela_login import TelaLogin  # importações normais

def main():
    print("Iniciando aplicativo da Clínica Especializada...")
    from app.db.setup import criar_banco
    criar_banco()
    app = TelaLogin()
    app.executar()

if __name__ == "__main__":
    main()