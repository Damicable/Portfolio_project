from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    author = fields.Nested('UserSchema', only=('id', 'username'))
    recipe = fields.Nested('RecipeSchema', only=('id', 'title'))
