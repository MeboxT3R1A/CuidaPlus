# app/db/login_bd.py
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
        print(f"[LOGIN] Usuário autenticado: {user[1]} ({user[2]})")
        return {"id": user[0], "nome": user[1], "papel": user[2]}
    print("[LOGIN] Falha de autenticação para:", email)
    return None

