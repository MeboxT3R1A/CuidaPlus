from app.db.connection import conectar

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senhaHash TEXT NOT NULL,
        papel TEXT CHECK(papel IN ('ADMIN', 'PACIENTE', 'COORDENACAO')) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Paciente (
        id INTEGER PRIMARY KEY,
        dataNascimento TEXT,
        tipoDeficiencia TEXT,
        FOREIGN KEY (id) REFERENCES Usuario(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Coordenacao (
        id INTEGER PRIMARY KEY,
        departamento TEXT,
        FOREIGN KEY (id) REFERENCES Usuario(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Atendimento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        observacoes TEXT,
        paciente_id INTEGER NOT NULL,
        coordenacao_id INTEGER NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES Paciente(id) ON DELETE CASCADE,
        FOREIGN KEY (coordenacao_id) REFERENCES Coordenacao(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Diagnostico (
        codigoCID TEXT PRIMARY KEY,
        descricao TEXT,
        atendimento_id INTEGER,
        FOREIGN KEY (atendimento_id) REFERENCES Atendimento(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Sugestao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT,
        prioridade TEXT CHECK(prioridade IN ('BAIXA', 'MEDIA', 'ALTA')),
        atendimento_id INTEGER,
        FOREIGN KEY (atendimento_id) REFERENCES Atendimento(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Relatorio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT CHECK(tipo IN ('PACIENTE', 'GERAL', 'COORDENACAO')),
        dataGeracao TEXT,
        conteudo TEXT,
        coordenacao_id INTEGER,
        FOREIGN KEY (coordenacao_id) REFERENCES Coordenacao(id) ON DELETE CASCADE
    );
    """)
    
    # Inserções básicas
    cursor.executescript("""
    INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES 
    (1, 'Administrador', 'admin@cuidamais.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'ADMIN'),
    (2, 'João Paciente', 'joao@paciente.com', 
    'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'PACIENTE'),
    (3, 'Maria Coordenação', 'maria@coord.com', '8c63a2fc2b14d8ae6f9d0bf2e2c4227ac2dc4bd84768e1259226b0c3d84f1c65', 'COORDENACAO');

    INSERT OR IGNORE INTO Paciente (id, dataNascimento, tipoDeficiencia)
    VALUES (2, '2000-05-10', 'Motora');

    INSERT OR IGNORE INTO Coordenacao (id, departamento)
    VALUES (3, 'Fisioterapia');

    INSERT OR IGNORE INTO Atendimento (id, data, observacoes, paciente_id, coordenacao_id)
    VALUES (1, '2025-10-15', 'Avaliação inicial de rotina', 2, 3);

    INSERT OR IGNORE INTO Diagnostico (codigoCID, descricao, atendimento_id)
    VALUES ('G80.0', 'Paralisia cerebral espástica', 1);

    INSERT OR IGNORE INTO Sugestao (id, texto, prioridade, atendimento_id)
    VALUES (1, 'Iniciar fisioterapia motora leve', 'ALTA', 1);

    INSERT OR IGNORE INTO Relatorio (id, tipo, dataGeracao, conteudo, coordenacao_id)
    VALUES (1, 'PACIENTE', '2025-10-15', 'Relatório inicial do paciente João.', 3);
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados criado e populado com sucesso.")

# Executa automaticamente se o arquivo for rodado direto
if __name__ == "__main__":
    criar_banco()
