from .auth_schemas import UserSchema
from .recipe_schemas import RecipeSchema
from .comment_schemas import CommentSchema
from .like_schemas import LikeSchema


like_schema = LikeSchema()
user_schema = UserSchema()
recipe_schema = RecipeSchema()
comment_schema = CommentSchema()

likes_schema = LikeSchema(many=True)
users_schema = UserSchema(many=True)
recipes_schema = RecipeSchema(many=True)
comments_schema = CommentSchema(many=True)