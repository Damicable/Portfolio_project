from app import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    recipes = db.relationship(
        'RecipeTag',
        backref='tag',
        cascade='all, delete',
        lazy=True,
    )