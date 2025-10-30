# app/db/setup.py
from app.db.connection import conectar

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""
    PRAGMA foreign_keys = ON;

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
    
    cursor.executescript(""" 
    -- Ativar chaves estrangeiras
    PRAGMA foreign_keys = ON;

    -- Inserir usuário administrador
    INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel)
    VALUES (1, 'Administrador', 'admin@cuidaplus.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'ADMIN');

    -- Inserir usuários pacientes
    INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES
    (2, 'Ana Souza', 'ana.souza@example.com', NULL, 'PACIENTE'),
    (3, 'Bruno Lima', 'bruno.lima@example.com', NULL, 'PACIENTE'),
    (4, 'Carla Mendes', 'carla.mendes@example.com', NULL, 'PACIENTE'),
    (5, 'Daniela Rocha', 'daniela.rocha@example.com', NULL, 'PACIENTE'),
    (6, 'Eduardo Pires', 'eduardo.pires@example.com', NULL, 'PACIENTE'),
    (7, 'Fernanda Alves', 'fernanda.alves@example.com', NULL, 'PACIENTE'),
    (8, 'Gabriel Torres', 'gabriel.torres@example.com', NULL, 'PACIENTE'),
    (9, 'Helena Martins', 'helena.martins@example.com', NULL, 'PACIENTE'),
    (10, 'Igor Nascimento', 'igor.nascimento@example.com', NULL, 'PACIENTE'),
    (11, 'Juliana Costa', 'juliana.costa@example.com', NULL, 'PACIENTE'),
    (14, 'Leonardo Ramos', 'leonardo.ramos@example.com', NULL, 'PACIENTE'),
    (15, 'Mariana Duarte', 'mariana.duarte@example.com', NULL, 'PACIENTE'),
    (16, 'Natália Oliveira', 'natalia.oliveira@example.com', NULL, 'PACIENTE'),
    (17, 'Otávio Freitas', 'otavio.freitas@example.com', NULL, 'PACIENTE'),
    (18, 'Priscila Barros', 'priscila.barros@example.com', NULL, 'PACIENTE'),
    (19, 'Rafael Gomes', 'rafael.gomes@example.com', NULL, 'PACIENTE'),
    (20, 'Sabrina Teixeira', 'sabrina.teixeira@example.com', NULL, 'PACIENTE'),
    (21, 'Tiago Ferreira', 'tiago.ferreira@example.com', NULL, 'PACIENTE'),
    (22, 'Vanessa Monteiro', 'vanessa.monteiro@example.com', NULL, 'PACIENTE');

    -- Inserir usuários da coordenação
    INSERT OR IGNORE INTO Usuario (id, nome, email, senhaHash, papel) VALUES
    (12, 'Dr. Marcos Tavares', 'marcos.tavares@example.com', NULL, 'COORDENACAO'),
    (13, 'Dra. Patrícia Lima', 'patricia.lima@example.com', NULL, 'COORDENACAO');

    -- Inserir pacientes
    INSERT OR IGNORE INTO Paciente (id, dataNascimento, tipoDeficiencia, responsavel) VALUES
    (2, '1998-03-15', 'Visual', 'Carlos Souza'),
    (3, '2002-07-22', 'Motora', 'Fernanda Lima'),
    (4, '1995-11-30', 'Auditiva', 'Marcos Mendes'),
    (5, '2000-05-09', 'Intelectual', 'Patrícia Rocha'),
    (6, '1988-12-01', 'Motora', 'João Pires'),
    (7, '1993-08-17', 'Visual', 'Mariana Alves'),
    (8, '1999-02-25', 'Auditiva', 'Paulo Torres'),
    (9, '2001-04-12', 'Intelectual', 'Sônia Martins'),
    (10, '1997-06-05', 'Motora', 'Roberta Nascimento'),
    (11, '2003-09-18', 'Visual', 'Cláudia Costa'),
    (14, '1994-02-03', 'Auditiva', 'Renata Ramos'),
    (15, '1996-10-11', 'Motora', 'André Duarte'),
    (16, '1992-01-28', 'Visual', 'Luciana Oliveira'),
    (17, '2004-07-19', 'Intelectual', 'Tatiane Freitas'),
    (18, '1990-12-09', 'Motora', 'Diego Barros'),
    (19, '1999-09-21', 'Auditiva', 'Cláudio Gomes'),
    (20, '2005-05-06', 'Intelectual', 'Elisa Teixeira'),
    (21, '1991-11-14', 'Visual', 'Henrique Ferreira'),
    (22, '1998-04-02', 'Motora', 'Cíntia Monteiro');

    -- Inserir informações complementares
    INSERT OR IGNORE INTO info (paciente_id, peso, altura, biografia, outras_observacoes) VALUES
    (2, 60.5, 1.65, 'Paciente com deficiência visual leve.', 'Utiliza bengala para locomoção.'),
    (3, 72.3, 1.75, 'Dificuldade motora em membros inferiores.', 'Em tratamento fisioterápico.'),
    (4, 58.0, 1.60, 'Surdez parcial desde a infância.', 'Usa aparelho auditivo.'),
    (5, 65.2, 1.68, 'Déficit cognitivo leve.', 'Participa de programas educacionais.'),
    (6, 80.1, 1.82, 'Lesão medular pós-acidente.', 'Em reabilitação contínua.'),
    (7, 55.4, 1.62, 'Cegueira total.', 'Usa cão-guia.'),
    (8, 68.9, 1.70, 'Perda auditiva moderada.', 'Realiza acompanhamento fonoaudiológico.'),
    (9, 74.0, 1.78, 'Transtorno intelectual leve.', 'Necessita acompanhamento psicopedagógico.'),
    (10, 69.5, 1.73, 'Mobilidade reduzida em perna direita.', 'Realiza fisioterapia semanal.'),
    (11, 57.2, 1.59, 'Baixa visão congênita.', 'Boa autonomia em ambientes conhecidos.'),
    (14, 63.7, 1.68, 'Surdez parcial adquirida.', 'Boa leitura labial.'),
    (15, 70.4, 1.76, 'Dificuldade de locomoção pós-fratura.', 'Recuperação estável.'),
    (16, 59.9, 1.64, 'Cegueira completa desde o nascimento.', 'Participa de grupos de apoio.'),
    (17, 75.8, 1.80, 'Déficit cognitivo moderado.', 'Necessita apoio familiar constante.'),
    (18, 82.2, 1.85, 'Amputação de membro inferior.', 'Usa prótese ortopédica.'),
    (19, 67.1, 1.71, 'Perda auditiva severa.', 'Aprendeu LIBRAS recentemente.'),
    (20, 64.5, 1.66, 'Transtorno de desenvolvimento leve.', 'Boa adaptação escolar.'),
    (21, 78.3, 1.79, 'Visão subnormal.', 'Usa lentes especiais.'),
    (22, 73.0, 1.75, 'Lesão motora parcial.', 'Realiza exercícios diários.');

    -- Inserir coordenações
    INSERT OR IGNORE INTO Coordenacao (id, departamento) VALUES
    (12, 'Fisioterapia'),
    (13, 'Psicologia');

    -- Inserir atendimentos
    INSERT OR IGNORE INTO Atendimento (id, data, observacoes, paciente_id, coordenacao_id) VALUES
    (1, '2025-09-10', 'Sessão de avaliação inicial.', 2, 12),
    (2, '2025-09-12', 'Acompanhamento psicológico.', 5, 13),
    (3, '2025-09-15', 'Revisão motora.', 3, 12),
    (4, '2025-09-20', 'Sessão de reforço cognitivo.', 9, 13),
    (5, '2025-09-25', 'Consulta de reavaliação.', 4, 12),
    (6, '2025-09-27', 'Sessão auditiva de acompanhamento.', 14, 13),
    (7, '2025-09-28', 'Revisão de mobilidade.', 15, 12),
    (8, '2025-09-30', 'Acompanhamento cognitivo.', 17, 13),
    (9, '2025-10-02', 'Sessão de prótese e marcha.', 18, 12),
    (10, '2025-10-05', 'Avaliação auditiva semestral.', 19, 13),
    (11, '2025-10-07', 'Treino de visão adaptativa.', 21, 12),
    (12, '2025-10-09', 'Revisão motora e postural.', 22, 12);

    -- Inserir diagnósticos
    INSERT OR IGNORE INTO Diagnostico (codigoCID, descricao, atendimento_id) VALUES
    ('H54', 'Cegueira e baixa visão', 1),
    ('G80', 'Paralisia cerebral', 3),
    ('F70', 'Retardo mental leve', 4),
    ('H90', 'Perda auditiva bilateral', 5),
    ('F71', 'Atraso mental moderado', 8),
    ('Z89', 'Amputação de membro inferior', 9),
    ('H91', 'Perda auditiva neurossensorial', 10),
    ('H53', 'Visão subnormal', 11),
    ('G81', 'Hemiparesia motora', 12);

    -- Inserir sugestões
    INSERT OR IGNORE INTO Sugestao (texto, prioridade, atendimento_id) VALUES
    ('Manter rotina de exercícios físicos leves.', 'MEDIA', 1),
    ('Aumentar frequência das sessões terapêuticas.', 'ALTA', 3),
    ('Avaliar progresso cognitivo mensalmente.', 'MEDIA', 4),
    ('Reforçar uso de aparelhos auditivos.', 'BAIXA', 5),
    ('Intensificar treinos de marcha.', 'MEDIA', 9),
    ('Introduzir sessões de grupo com outros pacientes.', 'BAIXA', 8),
    ('Acompanhar uso da prótese semanalmente.', 'ALTA', 9);

    -- Inserir relatórios
    INSERT OR IGNORE INTO Relatorio (tipo, dataGeracao, conteudo, coordenacao_id) VALUES
    ('GERAL', '2025-10-01', 'Relatório geral do mês de setembro.', 12),
    ('COORDENACAO', '2025-10-05', 'Atividades do setor de Psicologia.', 13),
    ('PACIENTE', '2025-10-07', 'Relatório individual de evolução do paciente Ana Souza.', 12),
    ('PACIENTE', '2025-10-15', 'Relatório de acompanhamento de Rafael Gomes.', 13),
    ('GERAL', '2025-10-20', 'Resumo das atividades multidisciplinares.', 12);
    """)


    conn.commit()
    conn.close()
    print("✅ Banco criado.")

