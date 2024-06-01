from app import app, db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(128), unique=True, nullable=False)
    recipes = db.relationship(
        "RecipeIngredient", backref=db.backref("ingredient", uselist=False), lazy=True
    )

    def to_dict(self):
        return {
            "english_name": self.english_name,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False, unique=False)
    bio = db.Column(db.Text, nullable=True, unique=False)
    recipes = db.relationship(
        "Recipe",
        backref=db.backref("contributor", uselist=False),
        cascade="all, delete",
        lazy=True,
    )
    collections = db.relationship(
        "Collection",
        backref=db.backref("user", uselist=False),
        cascade="all, delete",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
        }


Recipe_Tag = db.Table(
    "recipe_tag",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), nullable=False),
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id"), nullable=False),
)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    header_image = db.Column(db.String(128), nullable=True)
    prep_time = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(64), nullable=False)
    contributor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    steps = db.relationship(
        "RecipeStep",
        backref=db.backref("recipe", uselist=False),
        cascade="all, delete",
        lazy=True,
    )
    tags = db.relationship(
        "Tag", backref="recipes", secondary=Recipe_Tag, cascade="all, delete", lazy=True
    )
    ingredients = db.relationship(
        "RecipeIngredient",
        backref=db.backref("recipe", uselist=False),
        cascade="all, delete",
        lazy=False,
    )

    def __repr__(self):
        return f"<Recipe {self.id}: {self.name}>"


class RecipeStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    # recipe (backref)
    serial_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)


class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), nullable=False
    )
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(64), nullable=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


Collection_Recipe = db.Table(
    "collection_recipe",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collection.id"), nullable=False
    ),
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id"), nullable=False),
)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recipes = db.relationship(
        "Recipe", secondary=Collection_Recipe, backref="collections", lazy=True
    )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    is_reply = db.Column(db.Boolean, nullable=False)
    original_comment_id = db.Column(
        db.Integer, db.ForeignKey("comment.id"), nullable=True
    )
    date_time = db.Column(db.DateTime, nullable=False)
    

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "commenter_id": self.commenter_id,
            "is_reply": self.is_reply,
            "original_comment_id": self.original_comment_id,
        }
