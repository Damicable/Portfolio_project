from marshmallow import Schema, fields


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    ingredients = fields.Str(required=True)
    instructions = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    author = fields.Nested('UserSchema', only=('id', 'username'))
    comments = fields.List(fields.Nested('CommentSchema', exclude=('recipe',)))
    likes = fields.List(fields.Nested('LikeSchema', exclude=('recipe',)))

