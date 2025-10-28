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

def listar_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.nome, p.dataNascimento 
        FROM Usuario u
        JOIN Paciente p ON u.id = p.id
    """)
    pacientes = cursor.fetchall()  
    conn.close()
    return pacientes

#-------------------------------------

def listar():
    """Retorna todos os pacientes com informações básicas:
       (id, nome, dataNascimento, idade, tipoDeficiencia, email, responsavel)
    """
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
    """
    Cria um novo paciente. Espera um dicionário no formato:
    {
        'nome': str,
        'data_nasc': 'YYYY-MM-DD',
        'tipo_deficiencia': str,
        'contato': str,  # email
        'responsavel': str
    }
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Inserção em Usuario
        cursor.execute("""
            INSERT INTO Usuario (nome, email, senhaHash, papel)
            VALUES (?, ?, ?, 'PACIENTE')
        """, (dados['nome'], dados['contato'], "hash_fake"))
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
    """Atualiza dados de um paciente existente."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        # atualiza nome e email em Usuario
        cursor.execute("UPDATE Usuario SET nome=?, email=? WHERE id=?", (dados.get("nome"), dados.get("contato"), id_))
        # atualiza tipoDeficiencia e responsavel em Paciente
        cursor.execute("UPDATE Paciente SET tipoDeficiencia=?, responsavel=? WHERE id=?", 
                       (dados.get("tipo_de_deficiencia"), dados.get("responsavel"), id_))
        conn.commit()
        print(f"[LOG][paciente_bd.atualizar] Paciente ID={id_} atualizado.")
        return True
    except Exception as e:
        print("[ERRO][paciente_bd.atualizar]:", e)
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
