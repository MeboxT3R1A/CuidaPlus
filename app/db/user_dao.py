from .connection import conectar
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def autenticar_usuario(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, papel FROM Usuario WHERE email = ? AND senhaHash = ?",
        (email, hash_senha(senha))
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "nome": user[1], "papel": user[2]}
    return None

def cadastrar_usuario(nome, email, senha, papel):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Usuario (nome, email, senhaHash, papel) VALUES (?, ?, ?, ?)",
        (nome, email, hash_senha(senha), papel)
    )
    conn.commit()
    conn.close()
