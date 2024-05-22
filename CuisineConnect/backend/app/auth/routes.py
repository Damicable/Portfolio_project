from flask import Blueprint, request, jsonify
from app.models.user import User
from app.db import db
from werkzeug.security import generate_password_hash
from app.schemas.auth_schemas import user_schema, login_schema
from app.utils import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """ Register Route"""
    
    data = request.get_json()
    errors = user_schema.validate(data)
    
    if errors:
        return jsonify(errors), 400
    
    hashed_pwd = generate_password_hash(data.get('password'),
                                        method='scrypt',
                                        salt_length=12)
    user = User(username=data.get('username'),
                email=data.get('email'),
                password=hashed_pwd)
    db.session.add(user)
    db.session.commit()
    
    new_user = user_schema.dump(user)
    
    return jsonify(new_user), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login Route"""
    
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user = User.query.filter_by(username=data['username']).first()
    
    token = generate_token(user)
    return jsonify({"message": "Login successful", "token": token}), 200
