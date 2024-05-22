from app.db import db
from app.models.like import Like
from app.models.recipe import Recipe
from flask import Blueprint, jsonify
from flask_login import login_required, current_user

like_bp = Blueprint('likes', __name__)

@like_bp.route('/recipes/<int:recipe_id>/like', methods=['POST'])
@login_required
def like_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    
    like = Like.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if like:
        return jsonify({"message": "Recipe already liked"}), 400

    new_like = Like(user_id=current_user.id, recipe_id=recipe_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"message": "Recipe liked"}), 201

@like_bp.route('/recipes/<int:recipe_id>/unlike', methods=['DELETE'])
@login_required
def unlike_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    
    like = Like.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if not like:
        return jsonify({"message": "Recipe not liked yet"}), 400

    db.session.delete(like)
    db.session.commit()

    return jsonify({"message": "Recipe unliked"}), 200