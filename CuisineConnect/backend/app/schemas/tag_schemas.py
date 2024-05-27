from marshmallow import Schema, fields

class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    recipes = fields.List(fields.Nested('RecipeTagSchema', exclude=('tag',)), dump_only=True)