# app/db/setup.py
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
        responsavel TEXT,
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
        -- Usuários base
        INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES 
        (1, 'Administrador', 'a', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'ADMIN'),
        (2, 'João Paciente', 'joao@paciente.com', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'PACIENTE'),
        (3, 'Maria Coordenação', 'maria@coord.com', '8c63a2fc2b14d8ae6f9d0bf2e2c4227ac2dc4bd84768e1259226b0c3d84f1c65', 'COORDENACAO');

        -- Gera 50 pacientes (IDs 10–59)
        """ + "\n".join([
            f"INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES "
            f"({i}, 'Paciente {i}', 'paciente{i}@email.com', "
            f"'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'PACIENTE');"
            for i in range(1, 51)
        ]) + "\n" + "\n".join([
            f"INSERT OR IGNORE INTO Paciente (id, dataNascimento, tipoDeficiencia) VALUES "
            f"({i}, '200{(i%10)}-0{(i%9)+1}-15', "
            f"'Deficiência Tipo {i%5}');"
            for i in range(1, 51)
        ]) + """

        -- Gera 10 coordenadores (IDs 100–109)
        """ + "\n".join([
            f"INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES "
            f"({i}, 'Coordenador {i}', 'coord{i}@email.com', "
            f"'8c63a2fc2b14d8ae6f9d0bf2e2c4227ac2dc4bd84768e1259226b0c3d84f1c65', 'COORDENACAO');"
            for i in range(100, 110)
        ]) + "\n" + "\n".join([
            f"INSERT OR IGNORE INTO Coordenacao (id, departamento) VALUES ({i}, 'Departamento {i%3}');"
            for i in range(100, 110)
        ]) + """

        -- Gera 60 atendimentos, 1 diagnóstico e 1 sugestão por atendimento
        """ + "\n".join([
            f"INSERT OR IGNORE INTO Atendimento (id, data, observacoes, paciente_id, coordenacao_id) VALUES "
            f"({i}, '2025-10-{(i%28)+1:02d}', 'Atendimento de rotina {i}', {10 + (i%50)}, {100 + (i%10)});"
            for i in range(1, 61)
        ]) + "\n" + "\n".join([
            f"INSERT OR IGNORE INTO Diagnostico (codigoCID, descricao, atendimento_id) VALUES "
            f"('CID{i:03d}', 'Diagnóstico genérico {i}', {i});"
            for i in range(1, 61)
        ]) + "\n" + "\n".join([
            f"INSERT OR IGNORE INTO Sugestao (id, texto, prioridade, atendimento_id) VALUES "
            f"({i}, 'Sugestão de melhoria {i}', "
            f"CASE WHEN {i}%3=0 THEN 'ALTA' WHEN {i}%3=1 THEN 'MÉDIA' ELSE 'BAIXA' END, {i});"
            for i in range(1, 61)
        ]) + "\n" + "\n".join([
            f"INSERT OR IGNORE INTO Relatorio (id, tipo, dataGeracao, conteudo, coordenacao_id) VALUES "
            f"({i}, 'PACIENTE', '2025-10-{(i%28)+1:02d}', 'Relatório automático {i}', {100 + (i%10)});"
            for i in range(1, 61)
        ]) + ";"
        )


    conn.commit()
    conn.close()
    print("✅ Banco de dados criado e populado com sucesso.")

# Executa automaticamente se o arquivo for rodado direto
if __name__ == "__main__":
    criar_banco()
