# app/auth.py
from app.db.login_bd import hash_senha
from app.db.connection import conectar

_current_user = None

def set_current_user(user_dict):
    """
    user_dict: dicionário com pelo menos {'id', 'nome', 'email', 'papel'}.
    Deve ser chamado logo após autenticação bem-sucedida.
    """
    global _current_user
    _current_user = user_dict.copy() if user_dict else None

def get_current_user():
    return _current_user

def clear_current_user():
    global _current_user
    _current_user = None

def verify_password(user_id, senha_plaintext):
    """
    Verifica a senha do usuário comparando SHA256(senha_plaintext) com o campo senhaHash.
    Retorna True se bate, False caso contrário.
    """
    if user_id is None:
        return False
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SELECT senhaHash FROM Usuario WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            return False
        stored_hash = row[0] or ""
        return stored_hash == hash_senha(senha_plaintext)
    finally:
        conn.close()
