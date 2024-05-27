from app.db import db
from datetime import datetime


class Recipe(db.Model):
    """Recipe Model for Database Table"""
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    header_image = db.Column(db.String(256), nullable=True)
    prep_time = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    ingredients = db.relationship('RecipeIngredient', backref='recipe',
                                  lazy=False, cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='recipe',
                            lazy=True, cascade="all, delete-orphan")
    tags = db.relationship('RecipeTag', backref='recipe',
                            lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='recipe',
                               lazy=True, cascade="all, delete-orphan")
    
class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(16), nullable=False)

class RecipeTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
