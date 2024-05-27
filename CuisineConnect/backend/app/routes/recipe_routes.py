from app.db import db
from app.models.tag import Tag
from app.models.recipe import Recipe
from app.controller import createNewRecipe, updateRecipe
from app.models.ingredient import Ingredient
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.schemas import recipe_schema, recipes_schema
from app.models.recipe import Recipe, RecipeIngredient, RecipeTag


recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/recipes', methods=['POST'])
@login_required
def create_recipe():
    """Creates a Recipe"""
    
    data = request.get_json()
    errors = recipe_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_recipe = createNewRecipe(data, current_user)
    
    return jsonify(recipe_schema.dump(new_recipe)), 201

@recipes_bp.route('/recipes/<int:id>', methods=['PUT'])
@login_required
def update_recipe(id):
    """Updates a Recipe of id"""
    
    recipe = Recipe.query.get_or_404(id)

    if recipe.user_id != current_user.id:
        return jsonify({"message": "You do not have permission to update this recipe"}), 403

    data = request.get_json()
    errors = recipe_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    updateRecipe(recipe, data)

    return jsonify(recipe_schema.dump(recipe)), 200

@recipes_bp.route('/recipes/<int:id>', methods=['DELETE'])
@login_required
def delete_recipe(id):
    """Deletes a Recipe"""
    
    recipe = Recipe.query.get_or_404(id)

    if recipe.user_id != current_user.id:
        return jsonify({"message": "You do not have permission to delete this recipe"}), 403

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({"message": "Recipe deleted"}), 200

@recipes_bp.route('/recipes/<int:id>', methods=['GET'])
@login_required
def get_recipe(id):
    """Gets a particular recipe"""
    
    recipe = Recipe.query.get_or_404(id)
    
    return jsonify(recipe_schema.dump(recipe)), 200

@recipes_bp.route('/recipes', methods=['GET'])
@login_required
def get_recipes():
    """Gets all recipes"""
    
    recipes = Recipe.query.all()
    
    return jsonify(recipes_schema.dump(recipes)), 200
