from app.db import db
from app import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model for user table in the db
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    recipes = db.relationship('Recipe', backref='author',
                              lazy=True, cascade="all, delete")
    comments = db.relationship('Comment', backref='commentor',
                               lazy=True, cascade="all, delete")
    likes = db.relationship('Like', backref='user',
                            lazy=True, cascade="all, delete")
