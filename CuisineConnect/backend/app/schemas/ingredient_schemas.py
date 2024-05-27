from marshmallow import Schema, fields

class IngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    ingredient_name = fields.Str(required=True)
    recipes = fields.List(fields.Nested('RecipeIngredientSchema', exclude=('ingredient',)), dump_only=True)
