# app/db/paciente_bd.py
from app.db.connection import conectar
from datetime import date

def total_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Paciente")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def novos_pacientes(percentual=0.1):
    total = total_pacientes()
    return max(1, int(total * percentual))  # ao menos 1 paciente

def consultas_hoje():
    hoje = date.today().isoformat()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE data = ?", (hoje,))
    total = cursor.fetchone()[0]
    conn.close()
    return total

def listar():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.nome, p.dataNascimento
        FROM Usuario u
        JOIN Paciente p ON u.id = p.id
        WHERE u.papel = 'PACIENTE'
        ORDER BY u.id
    """)
    pacientes = cursor.fetchall()
    conn.close()
    return pacientes



#-------------------------------------

def listar_pacientes():
    """Retorna todos os pacientes com informações básicas."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT u.id, u.nome,
                   p.dataNascimento,
                   CAST((strftime('%Y', 'now') - strftime('%Y', p.dataNascimento)) AS INTEGER) AS idade,
                   p.tipoDeficiencia, u.email,
                   COALESCE(p.responsavel, 'Responsável não identificado') as responsavel
            FROM Usuario u
            JOIN Paciente p ON u.id = p.id
            WHERE u.papel = 'PACIENTE'
            ORDER BY u.id
        """)
        pacientes = cursor.fetchall()
        print(f"[LOG][paciente_bd.listar] {len(pacientes)} pacientes retornados.")
        return pacientes
    except Exception as e:
        print("[ERRO][paciente_bd.listar]:", e)
        return []
    finally:
        conn.close()

def salvar(dados):

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Usuario (nome, email, senhaHash, papel)
            VALUES (?, ?, ?, 'PACIENTE')
        """, (dados['nome'], dados['contato'], None))
        novo_id = cursor.lastrowid

        # Inserção em Paciente
        cursor.execute("""
            INSERT INTO Paciente (id, dataNascimento, tipoDeficiencia, responsavel)
            VALUES (?, ?, ?, ?)
        """, (novo_id, dados["data_nasc"], dados["tipo_deficiencia"], dados["responsavel"]))

        conn.commit()
        print(f"[LOG][paciente_bd.salvar] Paciente '{dados['nome']}' salvo com ID={novo_id}.")
        return True

    except Exception as e:
        print("[ERRO][paciente_bd.salvar]:", e)
        conn.rollback()
        return False
    finally:
        conn.close()

def atualizar(id_, dados):
    """Atualiza dados de um paciente existente (Usuario + Paciente)."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Atualiza dados na tabela Usuario
        cursor.execute("""
            UPDATE Usuario
            SET nome = ?, email = ?
            WHERE id = ?
        """, (dados.get("nome"), dados.get("contato"), id_))

        # Atualiza dados na tabela Paciente
        cursor.execute("""
            UPDATE Paciente
            SET dataNascimento = ?, tipoDeficiencia = ?, responsavel = ?
            WHERE id = ?
        """, (
            dados.get("data_nasc"),
            dados.get("tipo_deficiencia"),
            dados.get("responsavel"),
            id_
        ))

        conn.commit()
        print(f"[LOG][paciente_bd.atualizar] Paciente ID={id_} atualizado com sucesso.")
        return True

    except Exception as e:
        print(f"[ERRO][paciente_bd.atualizar]: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def excluir(id_):
    """Remove um paciente (e seu usuário correspondente)."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Paciente WHERE id=?", (id_,))
        cursor.execute("DELETE FROM Usuario WHERE id=?", (id_,))
        conn.commit()
        print(f"[LOG][paciente_bd.excluir] Paciente ID={id_} removido.")
        return True
    except Exception as e:
        print("[ERRO][paciente_bd.excluir]:", e)
        conn.rollback()
        return False
    finally:
        conn.close()

def obter_detalhes_paciente(id_paciente):
    """Retorna todas as informações detalhadas do paciente (Usuario, Paciente, Info, Atendimento)."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                u.id, u.nome, u.email,
                p.dataNascimento, 
                CAST((strftime('%Y', 'now') - strftime('%Y', p.dataNascimento)) AS INTEGER) AS idade,
                p.tipoDeficiencia, 
                p.responsavel,
                i.peso, i.altura, i.biografia, i.outras_observacoes,
                a.data AS ultima_data, a.observacoes AS ultima_obs,
                d.descricao AS diagnostico
            FROM Usuario u
            JOIN Paciente p ON u.id = p.id
            LEFT JOIN info i ON i.paciente_id = p.id
            LEFT JOIN Atendimento a ON a.paciente_id = p.id
            LEFT JOIN Diagnostico d ON d.atendimento_id = a.id
            WHERE u.id = ?
            ORDER BY a.data DESC
            LIMIT 1
        """, (id_paciente,))
        row = cursor.fetchone()
        if not row:
            return None
        keys = [
            "id", "nome", "email", "dataNascimento", "idade", "tipoDeficiencia", "responsavel",
            "peso", "altura", "biografia", "outras_observacoes",
            "ultima_data", "ultima_obs", "diagnostico"
        ]
        return dict(zip(keys, row))
    except Exception as e:
        print("[ERRO][paciente_bd.obter_detalhes_paciente]:", e)
        return None
    finally:
        conn.close()
