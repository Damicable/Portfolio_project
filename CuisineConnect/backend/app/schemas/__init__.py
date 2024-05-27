from .auth_schemas import UserSchema
from .like_schemas import LikeSchema
from .tag_schemas import TagSchema
from .comment_schemas import CommentSchema
from .ingredient_schemas import IngredientSchema
from .recipe_schemas import RecipeSchema, RecipeIngredientSchema, RecipeTagSchema


tags_schema = TagSchema()
like_schema = LikeSchema()
user_schema = UserSchema()
recipe_schema = RecipeSchema()
comment_schema = CommentSchema()
ingredients_schema = IngredientSchema()
recipe_ingredient_schema = RecipeIngredientSchema()

tags_schema = TagSchema(many=True)
likes_schema = LikeSchema(many=True)
users_schema = UserSchema(many=True)
recipes_schema = RecipeSchema(many=True)
comments_schema = CommentSchema(many=True)
ingredients_schema = IngredientSchema(many=True)
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
