from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.db import db
from app.models.comment import Comment
from app.schemas import comment_schema, comments_schema

comment_bp = Blueprint('comments', __name__)

@comment_bp.route('/recipes/<int:recipe_id>/comments', methods=['POST'])
@login_required
def add_comment(recipe_id):
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"message": "Content is required"}), 400

    new_comment = Comment(
        content=content,
        user_id=current_user.id,
        recipe_id=recipe_id
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify(comment_schema.dump(new_comment)), 201

@comment_bp.route('/recipes/<int:recipe_id>/comments', methods=['GET'])
def get_comments(recipe_id):
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    return jsonify(comments_schema.dump(comments)), 200
