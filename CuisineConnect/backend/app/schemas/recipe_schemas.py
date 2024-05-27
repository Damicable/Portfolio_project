from marshmallow import Schema, fields
from datetime import datetime


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    recipe_id = fields.Int(required=True)
    ingredient_id = fields.Int(required=True)
    quantity = fields.Float(required=True)
    unit = fields.Str(required=True)
    ingredient = fields.Nested('IngredientSchema', only=('id', 'ingredient_name'), dump_only=True)
    recipe = fields.Nested('RecipeSchema', only=('id', 'title'), dump_only=True)

class RecipeTagSchema(Schema):
    id = fields.Int(dump_only=True)
    recipe_id = fields.Int(required=True)
    tag_id = fields.Int(required=True)
    tag = fields.Nested('TagSchema', only=('id', 'name'), dump_only=True)
    recipe = fields.Nested('RecipeSchema', only=('id', 'title'), dump_only=True)

class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    header_image = fields.Str()
    prep_time = fields.Int(required=True)
    difficulty = fields.Int(required=True)
    vegetarian = fields.Bool(required=True)
    description = fields.Str(required=True)
    instructions = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True, default=datetime.now)
    author = fields.Nested('UserSchema', only=('id', 'username'), dump_only=True)
    ingredients = fields.List(fields.Nested(RecipeIngredientSchema), dump_only=True)
    tags = fields.List(fields.Nested(RecipeTagSchema), dump_only=True)
    comments = fields.List(fields.Nested('CommentSchema', exclude=('recipe',)), dump_only=True)
    likes = fields.List(fields.Nested('LikeSchema', exclude=('recipe',)), dump_only=True)
