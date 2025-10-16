from app.db.connection import conectar
from datetime import date, timedelta

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
    pacientes = cursor.fetchall()  # [(nome, dataNascimento), ...]
    conn.close()
    return pacientes
