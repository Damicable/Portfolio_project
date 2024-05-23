from app.db import db
from app.models.user import User
from app.utils import hash_password
from app.schemas import user_schema
from flask import Blueprint, request, jsonify
from app.schemas.auth_schemas import login_schema
from flask_login import login_user, logout_user, login_required


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """ Register Route"""
    
    data = request.get_json()
    errors = user_schema.validate(data)
    
    if errors:
        return jsonify(errors), 400
    
    hashed_pwd = hash_password(data.get('password'))
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
    
    login_user(user)
    return jsonify({"message": "Login successful"}), 200

@auth_bp.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout Route"""
    
    logout_user()
    return jsonify({"message": "Logout successful"}), 200
