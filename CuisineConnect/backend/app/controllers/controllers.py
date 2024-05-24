from app import db, bcrypt
from app.models import User, Recipe, Ingredient, Recipe_Step, Recipe_Tag, Recipe_Step, Recipe_Ingredient, Collection, Comment
from app.routes import *


def addFullRecipe(newRecipeFull: str, contributor_id: int, id=None):
    if id is None:
        newRecipe = Recipe(
            **{
                "name": newRecipeFull["name"],
                "prep_time": newRecipeFull["prep_time"],
                "description": newRecipeFull["description"],
                "difficulty": newRecipeFull["difficulty"],
                "contributor_id": contributor_id,
                "vegetarian": newRecipeFull["vegetarian"],
                "quantity": newRecipeFull["quantity"],
                "unit": newRecipeFull["unit"],
            }
        )
        db.session.add(newRecipe)
        db.session.commit()
        id = newRecipe.id
    else:
        db.session.add(
            Recipe(
                **{
                    "id": id,
                    "name": newRecipeFull["name"],
                    "prep_time": newRecipeFull["prep_time"],
                    "description": newRecipeFull["description"],
                    "difficulty": newRecipeFull["difficulty"],
                    "contributor_id": contributor_id,
                    "vegetarian": newRecipeFull["vegetarian"],
                    "quantity": newRecipeFull["quantity"],
                    "unit": newRecipeFull["unit"],
                }
            )
        )
        db.session.commit()

    for step in newRecipeFull["recipe_steps"]:
        db.session.add(
            Recipe_Step(
                **{
                    "recipe_id": id,
                    "serial_number": step["serial_number"],
                    "instruction": step["instruction"],
                }
            )
        )
    db.session.commit()

    for tag in newRecipeFull["recipe_tags"]:
        newTag = Tag.query.filter_by(name=tag["name"]).first()
        if newTag is None:
            newTag = Tag(**{"name": tag["name"]})
            db.session.add(newTag)
            db.session.commit()
        db.engine.execute(
            Recipe_Tag.insert().values(**{"tag_id": newTag.id, "recipe_id": id})
        )

    # add all the ingredients (if they don't exist already)
    for ingredient in newRecipeFull["recipe_ingredients"]:
        newIngredient = Ingredient.query.filter_by(
            english_name=ingredient["english_name"]
        ).first()
        if newIngredient is None:
            newIngredient = Ingredient(
                **{
                    "english_name": ingredient["english_name"],
                }
            )
            db.session.add(newIngredient)
            db.session.commit()

        db.session.add(
            Recipe_Ingredient(
                **{
                    "recipe_id": id,
                    "ingredient_id": newIngredient.id,
                    "quantity": ingredient["quantity"],
                    "unit": ingredient["unit"],
                }
            )
        )
    db.session.commit()


# TODO: create a proper function to edit recipes which compares it to the existing one
# the existing method just deletes the old one and creates a new one in its place
def editRecipe(newRecipeFull, recipe: Recipe, user: User):
    id = recipe.id
    db.session.delete(recipe)
    db.session.commit()
    addFullRecipe(newRecipeFull, user.id, id)


def addNewUser(newUser: dict):
    newUser["password"] = bcrypt.generate_password_hash(
        newUser["password"].encode("utf-8")
    )
    user = User(**newUser)
    db.session.add(user)
    db.session.commit()
    db.session.add(Collection(**{"name": "favorites", "user_id": user.id}))
    db.session.commit()


def getRecipeById(id: int) -> Recipe:
    return Recipe.query.get(id)


def getNextOf(id: int) -> int:
    ids = [recipe.id for recipe in Recipe.query.all()]
    next_id = 0
    for i in ids:
        if i > id:
            next_id = i
            break
    # print(f"next of {id}: {next_id}")
    return next_id


def getPrevOf(id: int) -> int:
    ids = [recipe.id for recipe in Recipe.query.all()]
    prev_id = 0
    for i in ids:
        if i < id and i > prev_id:
            prev_id = i
        elif i >= id:
            break
    # print(f"prev of {id}: {prev_id}")
    return prev_id


def getRecipeMeta(recipeById: Recipe):
    return {
        "id": recipeById.id,
        "name": recipeById.name,
        "prep_time": recipeById.prep_time,
        "description": recipeById.description,
        "difficulty": recipeById.difficulty,
        "vegetarian": recipeById.vegetarian,
        "quantity": recipeById.quantity,
        "unit": recipeById.unit,
        "contributor_username": recipeById.contributor.username,
        "next_id": getNextOf(recipeById.id),
        "prev_id": getPrevOf(recipeById.id),
    }


def getRecipeIngredients(recipe: Recipe):
    return [
        {
            "english_name": recipe_ingredient.ingredient.english_name,
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit,
        }
        for recipe_ingredient in recipe.ingredients
    ]


def getRecipeTags(recipe: Recipe):
    return [tag.name for tag in recipe.tags]


def getRecipeSteps(recipe: Recipe):
    steps = recipe.steps.sort(key=lambda step: step.serial_number)
    return [step.instruction for step in recipe.steps]


def getContributor(recipe: Recipe):
    return {
        "contributor_name": recipe.contributor.name,
        "contributor_username": recipeById.contributor.username,
        "contributor_bio": recipe.contributor.bio,
    }


def getRecipeFull(recipeById: Recipe):
    return {
        "id": recipeById.id,
        "name": recipeById.name,
        "prep_time": recipeById.prep_time,
        "description": recipeById.description,
        "difficulty": recipeById.difficulty,
        "vegetarian": recipeById.vegetarian,
        "quantity": recipeById.quantity,
        "unit": recipeById.unit,
        "contributor_name": recipeById.contributor.name,
        "contributor_username": recipeById.contributor.username,
        "contributor_bio": recipeById.contributor.bio,
        "recipe_tags": getRecipeTags(recipeById),
        "recipe_ingredients": getRecipeIngredients(recipeById),
        "recipe_steps": getRecipeSteps(recipeById),
        "next_id": getNextOf(recipeById.id),
        "prev_id": getPrevOf(recipeById.id),
    }


def getCommentsTreeForRecipe(recipe: Recipe):
    comments = Comment.query.filter(Comment.recipe_id == recipe.id)
    coms = {
        com.id: {
            "id": com.id,
            "text": com.text,
            "commenter": User.query.filter(User.id == com.commenter_id).first().username,
            "is_reply": com.is_reply,
            "reply_to": com.original_comment_id,
            "replies": [],
        }
        for com in comments
    }
    remove_list = []
    for id, com in coms.items():
        if com["is_reply"]:
            coms[com['reply_to']]["replies"].append(com)
            remove_list.append(id)
    for id in remove_list:
        del coms[id]
    coms = [coms[id] for id in coms]
    for com in coms:
        del com['is_reply']
        del com['reply_to']
    return coms