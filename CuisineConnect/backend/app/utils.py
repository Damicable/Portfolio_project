from . import bcrypt


def hash_password(password):
    """creates a hashed password from pasword"""
    hashed_pwd = bcrypt.generate_password_hash(password).decode("utf-8")
    
    return hashed_pwd
