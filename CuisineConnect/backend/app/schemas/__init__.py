from .auth_schemas import UserSchema
from .recipe_schemas import RecipeSchema
from .comment_schemas import CommentSchema
from .like_schemas import LikeSchema


user_schema = UserSchema()
users_schema = UserSchema(many=True)
recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)