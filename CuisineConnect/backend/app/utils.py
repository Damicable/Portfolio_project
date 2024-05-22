import jwt
from datetime import datetime, timedelta
from app.config import config
from . import bcrypt

def generate_token(user):
    """Genetates JWT tokens"""
    
    payload = {
        'user_id': user.id,
        'exp': datetime.now() + timedelta(seconds=config.JWT_EXPIRATION_DELTA)
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token

def hash_password(password):
    """creates a hashed password from pasword"""
    hashed_pwd = bcrypt.generate_password_hash(password).decode("utf-8")
    
    return hashed_pwd
