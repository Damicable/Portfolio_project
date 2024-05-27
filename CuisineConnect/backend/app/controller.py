from app.db import db
from app.models.tag import Tag
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeIngredient, RecipeTag


def createNewRecipe(data, current_user):
    """Creates Recipe"""
    
    new_recipe = Recipe(
        title=data['title'],
        header_image=data.get('header_image'),
        prep_time=data['prep_time'],
        difficulty=data['difficulty'],
        vegetarian=data['vegetarian'],
        description=data['description'],
        instructions=data['instructions'],
        user_id=current_user.id
    )

    db.session.add(new_recipe)
    db.session.commit()
    
    # Add ingredients
    for ingredient_data in data.get('ingredients', []):
        ingredient = Ingredient.query.get(ingredient_data['ingredient_id'])
        if ingredient:
            recipe_ingredient = RecipeIngredient(
                recipe_id=new_recipe.id,
                ingredient_id=ingredient.id,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )
            db.session.add(recipe_ingredient)

    # Add tags
    for tag_data in data.get('tags', []):
        tag = Tag.query.get(tag_data['tag_id'])
        if tag:
            recipe_tag = RecipeTag(
                recipe_id=new_recipe.id,
                tag_id=tag.id
            )
            db.session.add(recipe_tag)

    db.session.commit()
    
    return new_recipe

def updateRecipe(recipe : Recipe, data):
    """Updates a recipe"""
    
    recipe.title = data['title']
    recipe.description = data['description']
    recipe.instructions = data['instructions']
    recipe.header_image = data.get('header_image', recipe.header_image)
    recipe.prep_time = data['prep_time']
    recipe.difficulty = data['difficulty']
    recipe.vegetarian = data['vegetarian']

    # Update ingredients
    new_ingredients = {i['ingredient_id']: i for i in data['ingredients']}
    current_ingredients = {ri.ingredient_id: ri for ri in recipe.ingredients}

    # Add or update ingredients
    for ingredient_id, ingredient_data in new_ingredients.items():
        if ingredient_id in current_ingredients:
            # Update existing ingredient
            current_ingredients[ingredient_id].quantity = ingredient_data['quantity']
            current_ingredients[ingredient_id].unit = ingredient_data['unit']
        else:
            # Add new ingredient
            new_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient_id,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )
            db.session.add(new_ingredient)

    # Remove deleted ingredients
    for ingredient_id in current_ingredients:
        if ingredient_id not in new_ingredients:
            db.session.delete(current_ingredients[ingredient_id])

    # Update tags
    new_tags = {t['tag_id']: t for t in data['tags']}
    current_tags = {rt.tag_id: rt for rt in recipe.tags}

    # Add or update tags
    for tag_id, tag_data in new_tags.items():
        if tag_id not in current_tags:
            # Add new tag
            new_tag = RecipeTag(
                recipe_id=recipe.id,
                tag_id=tag_id
            )
            db.session.add(new_tag)

    # Remove deleted tags
    for tag_id in current_tags:
        if tag_id not in new_tags:
            db.session.delete(current_tags[tag_id])

    db.session.commit()
