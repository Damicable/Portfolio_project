from app import db, bcrypt
from app.models import (
    User, Recipe,
    Ingredient, RecipeStep,
    Recipe_Tag, RecipeIngredient,
    Collection, Comment, Tag
    )


def add_full_recipe(new_recipe_full: dict, contributor_id: int, recipe_id=None):
    if recipe_id is None:
        new_recipe = Recipe(
            name=new_recipe_full["name"],
            header_image=new_recipe_full["header_image"],
            prep_time=new_recipe_full["prep_time"],
            description=new_recipe_full["description"],
            difficulty=new_recipe_full["difficulty"],
            contributor_id=contributor_id,
            vegetarian=new_recipe_full["vegetarian"],
            quantity=new_recipe_full["quantity"],
            unit=new_recipe_full["unit"]
        )
        db.session.add(new_recipe)
        db.session.commit()
        recipe_id = new_recipe.id
    else:
        new_recipe = Recipe(
            id=recipe_id,
            name=new_recipe_full["name"],
            prep_time=new_recipe_full["prep_time"],
            description=new_recipe_full["description"],
            difficulty=new_recipe_full["difficulty"],
            contributor_id=contributor_id,
            vegetarian=new_recipe_full["vegetarian"],
            quantity=new_recipe_full["quantity"],
            unit=new_recipe_full["unit"]
        )
        db.session.add(new_recipe)
        db.session.commit()

    # Add recipe steps
    for step in new_recipe_full["recipe_steps"]:
        recipe_step = RecipeStep(
            recipe_id=recipe_id,
            serial_number=step["serial_number"],
            instruction=step["instruction"]
        )
        db.session.add(recipe_step)
    db.session.commit()

    # Add recipe tags
    for tag in new_recipe_full["recipe_tags"]:
        new_tag = Tag.query.filter_by(name=tag["name"]).first()
        if new_tag is None:
            new_tag = Tag(name=tag["name"])
            db.session.add(new_tag)
            db.session.commit()
        db.session.execute(Recipe_Tag.insert().values(tag_id=new_tag.id, recipe_id=recipe_id))
    db.session.commit()

    # Add recipe ingredients
    for ingredient in new_recipe_full["recipe_ingredients"]:
        new_ingredient = Ingredient.query.filter_by(english_name=ingredient["english_name"]).first()
        if new_ingredient is None:
            new_ingredient = Ingredient(english_name=ingredient["english_name"])
            db.session.add(new_ingredient)
            db.session.commit()
        
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=new_ingredient.id,
            quantity=ingredient["quantity"],
            unit=ingredient["unit"]
        )
        db.session.add(recipe_ingredient)
    db.session.commit()
    
    return new_recipe


# This method just deletes the old one and creates a new one in its place
def edit_recipe(new_recipe_full, recipe: Recipe, user: User):
    recipe_id = recipe.id
    db.session.delete(recipe)
    db.session.commit()
    add_full_recipe(new_recipe_full, user.id, recipe_id)


def add_new_user(new_user: dict):
    new_user["password"] = bcrypt.generate_password_hash(
        new_user["password"].encode("utf-8")
    )
    user = User(**new_user)
    db.session.add(user)
    db.session.commit()
    db.session.add(Collection(**{"name": "favorites", "user_id": user.id}))
    db.session.commit()
    
    return user.to_dict()


def get_recipe_by_id(id: int) -> Recipe:
    print(id)
    return Recipe.query.get(id)


def get_recipe_tags(recipe: Recipe):
            return [tag.name for tag in recipe.tags]


def get_next_of(id: int) -> int:
    ids = [recipe.id for recipe in Recipe.query.all()]
    next_id = 0
    for i in ids:
        if i > id:
            next_id = i
            break
    # print(f"next of {id}: {next_id}")
    return next_id


def get_prev_of(id: int) -> int:
    ids = [recipe.id for recipe in Recipe.query.all()]
    prev_id = 0
    for i in ids:
        if i < id and i > prev_id:
            prev_id = i
        elif i >= id:
            break
    # print(f"prev of {id}: {prev_id}")
    return prev_id


def get_recipe_meta(recipe_by_id: Recipe):
    return {
        "id": recipe_by_id.id,
        "name": recipe_by_id.name,
        "prep_time": recipe_by_id.prep_time,
        "description": recipe_by_id.description,
        "difficulty": recipe_by_id.difficulty,
        "vegetarian": recipe_by_id.vegetarian,
        "quantity": recipe_by_id.quantity,
        "unit": recipe_by_id.unit,
        "contributor_username": recipe_by_id.contributor.username,
        "next_id": get_next_of(recipe_by_id.id),
        "prev_id": get_prev_of(recipe_by_id.id),
    }


def get_recipe_ingredients(recipe: Recipe):
    return [
        {
            "english_name": recipe_ingredient.ingredient.english_name,
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit,
        }
        for recipe_ingredient in recipe.ingredients
    ]


def get_recipe_steps(recipe: Recipe):
    recipe.steps.sort(key=lambda step: step.serial_number)
    return [step.instruction for step in recipe.steps]


def get_contributor(recipe: Recipe):
    return {
        "contributor_name": recipe.contributor.name,
        "contributor_username": recipe.contributor.username,
        "contributor_bio": recipe.contributor.bio,
    }


def get_recipe_full(recipe: Recipe):
    return {
        "id": recipe.id,
        "name": recipe.name,
        "prep_time": recipe.prep_time,
        "description": recipe.description,
        "difficulty": recipe.difficulty,
        "vegetarian": recipe.vegetarian,
        "quantity": recipe.quantity,
        "unit": recipe.unit,
        "contributor_name": recipe.contributor.name,
        "contributor_username": recipe.contributor.username,
        "contributor_bio": recipe.contributor.bio,
        "recipe_tags": get_recipe_tags(recipe),
        "recipe_ingredients": get_recipe_ingredients(recipe),
        "recipe_steps": get_recipe_steps(recipe),
        "next_id": get_next_of(recipe.id),
        "prev_id": get_prev_of(recipe.id),
    }


def get_comments_tree_for_recipe(recipe: Recipe):
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