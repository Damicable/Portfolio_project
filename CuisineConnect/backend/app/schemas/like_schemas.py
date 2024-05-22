from marshmallow import Schema, fields

class LikeSchema(Schema):
    id = fields.Int(dump_only=True)
    user = fields.Nested('UserSchema', only=('id', 'username'))
    recipe = fields.Nested('RecipeSchema', only=('id', 'title'))
