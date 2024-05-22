import re
from marshmallow import ValidationError
from app.models.user import User
from app import bcrypt


def validate_password(password: str) -> None:
    """
    Password Validator 
    """
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")
        
def validate_email(email):
    """Email Validator"""
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValidationError("Invalid email address.")

def validate_credentials(data):
    """Credential Validator"""
    
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValidationError("Invalid username or password.")

    if not bcrypt.check_password_hash(user.password, password):
        raise ValidationError("Invalid username or password.")
