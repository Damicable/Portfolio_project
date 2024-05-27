from app import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(128), unique=True, nullable=False)
    recipes = db.relationship(
        "RecipeIngredient", backref="ingredients", lazy=True
    )