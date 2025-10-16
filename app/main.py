from app.ui.login import LoginTela

def main():
    """
    Função principal que inicializa e executa o aplicativo
    """
    print("Iniciando aplicativo da Clínica Especializada...")
    app = LoginTela()
    app.executar()

if __name__ == "__main__":
    main()