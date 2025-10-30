# app/db/setup.py
from app.db.connection import conectar

HASH_SENHA_A = "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"


def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senhaHash TEXT,
        papel TEXT CHECK(papel IN ('ADMIN', 'PACIENTE', 'COORDENACAO')) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Paciente (
        id INTEGER PRIMARY KEY,
        dataNascimento TEXT,
        tipoDeficiencia TEXT,
        responsavel TEXT,
        FOREIGN KEY (id) REFERENCES Usuario(id) ON DELETE CASCADE
    );
        
    CREATE TABLE IF NOT EXISTS info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL UNIQUE,
        peso REAL,
        altura REAL,
        biografia TEXT,
        outras_observacoes TEXT,
        criado_em TEXT DEFAULT (datetime('now')),
        atualizado_em TEXT,
        FOREIGN KEY (paciente_id) REFERENCES Paciente(id) ON DELETE CASCADE
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
    
    # Limpa conteúdos antigos (opcional, seguro: apaga todas as linhas)
    # Se você prefere manter dados antigos, comente os DELETEs abaixo.
    cursor.executescript("""
        DELETE FROM Relatorio;
        DELETE FROM Sugestao;
        DELETE FROM Diagnostico;
        DELETE FROM Atendimento;
        DELETE FROM info;
        DELETE FROM Paciente;
        DELETE FROM Coordenacao;
        DELETE FROM Usuario;
    """)

    # Inserções manuais e mínimas (usuário de teste "a" com senha "a")
    cursor.executescript(f"""
        -- Usuário de teste (nome "a", senha "a" -> hash SHA-256)
        INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel)
        VALUES (1, 'a', 'a', '{HASH_SENHA_A}', 'ADMIN');

        -- Exemplos de pacientes (criados manualmente)
        INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES
            (2, 'João Silva', 'joao.silva@example.com', '{HASH_SENHA_A}', 'PACIENTE'),
            (3, 'Maria Santos', 'maria.santos@example.com', '{HASH_SENHA_A}', 'PACIENTE'),
            (4, 'Pedro Oliveira', 'pedro.oliveira@example.com', '{HASH_SENHA_A}', 'PACIENTE'),
            (5, 'Ana Costa', 'ana.costa@example.com', '{HASH_SENHA_A}', 'PACIENTE');

        INSERT OR IGNORE INTO Paciente (id, dataNascimento, tipoDeficiencia, responsavel) VALUES
            (2, '1990-05-12', 'Deficiência Visual', 'Responsável: Carlos Silva'),
            (3, '1985-11-23', 'Deficiência Auditiva', 'Responsável: Carla Santos'),
            (4, '2002-07-04', 'Deficiência Motora', 'Responsável: Luciana Oliveira'),
            (5, '1978-02-19', 'Deficiência Intelectual', 'Responsável: Marcos Costa');

        -- Alguns registros 'info' de exemplo (opcional)
        INSERT OR IGNORE INTO info (paciente_id, peso, altura, biografia) VALUES
            (2, 72.5, 1.75, 'Paciente com histórico de acompanhamento oftalmológico.'),
            (3, 65.0, 1.68, 'Atendimento fonoaudiológico periódico.'),
            (5, 80.0, 1.70, 'Paciente com necessidades de suporte social.');

        -- Exemplo de coordenacao mínima e um atendimento/diagnóstico para um paciente
        INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES
            (100, 'Coordenador Exemplo', 'coord@example.com', '{HASH_SENHA_A}', 'COORDENACAO');
        INSERT OR IGNORE INTO Coordenacao (id, departamento) VALUES (100, 'Departamento Exemplo');

        INSERT OR IGNORE INTO Atendimento (id, data, observacoes, paciente_id, coordenacao_id) VALUES
            (1, date('now'), 'Consulta inicial de rotina', 2, 100);

        INSERT OR IGNORE INTO Diagnostico (codigoCID, descricao, atendimento_id) VALUES
            ('CID001', 'Diagnóstico de exemplo', 1);
    """)

    # === Gerar massa de teste: ajuste start_id e quantidade ===
    start_id = 200       # comece em um número que não conflite com seus IDs existentes
    quantidade = 100     # quantos pacientes quer criar

    for i in range(quantidade):
        uid = start_id + i
        nome = f"Paciente {uid}"
        email = f"paciente{uid}@example.com"
        senha_hash = HASH_SENHA_A  # usa o hash já definido no setup
        papel = "PACIENTE"

        # usuario
        cursor.execute("""
            INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel)
            VALUES (?, ?, ?, ?, ?)
        """, (uid, nome, email, senha_hash, papel))

        # paciente (data de nascimento variada para testes)
        ano = 1950 + (i % 60)          # 1950..2009
        mes = (i % 12) + 1
        dia = ((i % 28) + 1)
        data_nasc = f"{ano:04d}-{mes:02d}-{dia:02d}"
        tipo_def = f"Deficiência Tipo {i % 5}"
        responsavel = f"Responsável {uid}"
        cursor.execute("""
            INSERT OR IGNORE INTO Paciente (id, dataNascimento, tipoDeficiencia, responsavel)
            VALUES (?, ?, ?, ?)
        """, (uid, data_nasc, tipo_def, responsavel))

        # info (peso/altura simples)
        peso = 50 + (i % 60) * 0.5     # 50.0 .. 79.5 por exemplo
        altura = 1.50 + (i % 60) * 0.01
        biografia = f"Biografia de teste do paciente {uid}."
        cursor.execute("""
            INSERT OR IGNORE INTO info (paciente_id, peso, altura, biografia)
            VALUES (?, ?, ?, ?)
        """, (uid, peso, altura, biografia))

        # um atendimento de exemplo (ligado à coordenacao_id 100 criada no setup)
        data_at = f"2025-10-{((i % 28) + 1):02d}"
        obs = f"Atendimento de teste {uid}"
        cursor.execute("""
            INSERT OR IGNORE INTO Atendimento (data, observacoes, paciente_id, coordenacao_id)
            VALUES (?, ?, ?, ?)
        """, (data_at, obs, uid, 100))

    conn.commit()
    conn.close()
    print("✅ Banco de dados criado e populado com sucesso.")

# Executa automaticamente se o arquivo for rodado direto
if __name__ == "__main__":
    criar_banco()
