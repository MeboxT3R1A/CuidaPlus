# app/main.py
from app.ui.login import LoginTela
from app.db.setup import criar_banco

def main():
    print("Iniciando aplicativo da Clínica Especializada...")
    from app.db.setup import criar_banco
    criar_banco()
    app = LoginTela()
    app.executar()

if __name__ == "__main__":
    main()