from datetime import datetime
from app.db import db


class Recipe(db.Model):
    """Recipe Model for Database Table"""
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now())
