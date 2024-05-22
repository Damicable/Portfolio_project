import jwt
from datetime import datetime, timedelta
from app.config import config

def generate_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.now() + timedelta(seconds=config.JWT_EXPIRATION_DELTA)
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token