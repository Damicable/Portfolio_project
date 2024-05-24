from datetime import datetime, timedelta, timezone
import json

from flask import jsonify, request, abort, Response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
)

from app import app, bcrypt
from app.models import Recipe, User


@app.route("/api/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        newUser = request.get_json(force=True)
        user = User.query.filter(User.username == newUser["username"]).first()
        print(newUser)
        if user is None:
            addNewUser(newUser)
            return Response(status=201)
        else:
            return Response(status=201)

    else:
        return jsonify([user.to_dict() for user in User.query.all()])


@app.route("/api/users/login", methods=["POST"])
def user_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None).encode("utf-8")
    user = User.query.filter(User.username == username).first()
    if user is not None and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token})
    else:
        abort(401)


@app.route("/api/users/profile")
@jwt_required()
def user_profile():
    username = get_jwt_identity()
    return jsonify(User.query.filter(User.username == username).first().to_dict())


@app.route("/api/users/logout")
def user_logout():
    response = Response(status=202)
    unset_jwt_cookies(response)
    return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=15))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
            else:
                response.data = json.dumps({"access_token": access_token})
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@app.route("/api/users/<username>")
def users_str(username):
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app.route("/api/users/<username>/recipes")
def user_str_recipes(username):
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)
    else:
        return jsonify(
            {
                "recipes": [
                    getRecipeMeta(recipe)
                    for recipe in Recipe.query.filter(
                        Recipe.contributor.has(User.username == user.username)
                    )
                ]
            }
        )


@app.route("/api/users/<username>/recipes/full")
def user_str_recipes_full(username):
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)
    else:
        return jsonify(
            {
                "recipes": [
                    getRecipeFull(recipe)
                    for recipe in Recipe.query.filter(
                        Recipe.contributor.has(User.username == user.username)
                    )
                ]
            }
        )


@app.route("/api/collections", methods=["GET", "POST", "DELETE"])
@jwt_required()
def user_collections():
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)
    else:
        if request.method == "GET":
            return jsonify(
                {
                    "collections": [
                        {
                            "name": c.name,
                            "recipes": [getRecipeMeta(r) for r in c.recipes],
                        }
                        for c in user.collections
                    ]
                }
            )
        if request.method == "POST":
            collection_name = request.json.get("collection_name", None)
            collection = (
                Collection.query.filter(Collection.user_id == user.id)
                .filter(Collection.name == collection_name)
                .first()
            )
            if collection is None:
                db.session.add(
                    Collection(**{"name": collection_name, "user_id": user.id})
                )
                db.session.commit()
                return Response(status=201)
            else:
                return Response(status=202)
        if request.method == "DELETE":
            collection_name = request.json.get("collection_name", None)
            collection = (
                Collection.query.filter(Collection.user_id == user.id)
                .filter(Collection.name == collection_name)
                .first()
            )
            if collection is not None:
                db.session.query(Collection_Recipe).filter_by(
                    collection_id=collection.id
                ).delete()
                db.session.delete(collection)
                db.session.commit()
                return Response(status=201)
            else:
                return Response(status=202)


@app.route("/api/collections/<collection_name>", methods=["GET", "POST", "DELETE"])
@jwt_required()
def user_collection(collection_name):
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    collection = (
        Collection.query.filter(Collection.user_id == user.id)
        .filter(Collection.name == collection_name)
        .first()
    )
    if user is None or collection is None:
        abort(404)
    if request.method == "GET":
        return jsonify(
            {"recipes": [getRecipeMeta(recipe) for recipe in collection.recipes]}
        )
    if request.method == "POST":
        recipe_id = request.json.get("recipe_id", None)
        recipe = Recipe.query.get(recipe_id)
        if recipe is None:
            abort(404)
        else:
            if recipe.id in [r.id for r in collection.recipes]:
                return Response(status=202)
            else:
                db.engine.execute(
                    Collection_Recipe.insert().values(
                        **{"collection_id": collection.id, "recipe_id": recipe.id}
                    )
                )
                return Response(status=201)
    if request.method == "DELETE":
        recipe_id = request.json.get("recipe_id", None)
        recipe = Recipe.query.get(recipe_id)
        if recipe is None:
            abort(404)
        else:
            if recipe.id not in [r.id for r in collection.recipes]:
                return Response(status=202)
            else:
                db.session.query(Collection_Recipe).filter_by(
                    collection_id=collection.id
                ).filter_by(recipe_id=recipe_id).delete()
                db.session.commit()
                return Response(status=201)


@app.route("/api/recipes", methods=["POST"])
@jwt_required()
def recipes():
    newRecipeFull = request.get_json(force=True)
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    print(newRecipeFull)
    print(username)
    if user is None:
        return Response(status=400)
    else:
        addFullRecipe(newRecipeFull, user.id)
        return Response(status=201)


@app.route("/api/recipes/<int:num>", methods=["GET"])
def recipes_n(num):
    r = getRecipeById(num)
    if r is None:
        abort(404)
    else:
        return jsonify(getRecipeMeta(r))


@app.route("/api/recipes/<int:num>", methods=["PATCH", "DELETE"])
@jwt_required()
def recipes_n_path_delete(num):
    r = getRecipeById(num)
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    if r is None or user is None or user.username != r.contributor.username:
        abort(404)
    else:
        if request.method == "PATCH":
            newRecipeFull = request.get_json(force=True)
            editRecipe(newRecipeFull, r, user)
            return Response(status=200)
        if request.method == "DELETE":
            db.session.delete(r)
            db.session.commit()
            return Response(status=200)


@app.route("/api/recipes/<int:num>/tags")
def recipes_n_tags(num):
    r = getRecipeById(num)
    if r is None:
        abort(404)
    else:
        return jsonify({"tags": getRecipeTags(r)})


@app.route("/api/recipes/<int:num>/ingredients")
def recipes_n_ingredients(num):
    r = getRecipeById(num)
    if r is None:
        abort(404)
    else:
        return jsonify({"name": r.name, "recipe_ingredients": getRecipeIngredients(r)})


@app.route("/api/recipes/<int:num>/steps")
def recipes_n_steps(num):
    r = getRecipeById(num)
    if r is None:
        abort(404)
    else:
        return jsonify({"name": r.name, "recipe_steps": getRecipeSteps(r)})


@app.route("/api/recipes/<int:num>/full")
def recipes_n_full(num):
    r = getRecipeById(num)
    if r is None:
        abort(404)
    else:
        return jsonify(getRecipeFull(r))


@app.route("/api/recipes/count")
def recipes_count():
    return jsonify({"count": len(Recipe.query.all())})


@app.route("/api/recipes/all")
def recipes_all():
    return jsonify(
        {"recipes": [getRecipeMeta(recipe) for recipe in Recipe.query.all()]}
    )


@app.route("/api/recipes/bytag/<tag>")
def recipes_bytag(tag):
    return jsonify(
        {
            "recipes": [
                getRecipeMeta(r)
                for r in Tag.query.filter(Tag.name == tag).first().recipes
            ]
        }
    )


@app.route("/api/ingredients/all")
def ingredients_all():
    return jsonify({"ingredients": [i.to_dict() for i in Ingredient.query.all()]})


@app.route("/api/tags/all")
def tags_all():
    return jsonify({"tags": [t.name for t in Tag.query.all()]})


@app.route("/api/recipes/<int:recipe_id>/comments/add", methods=["POST"])
@jwt_required()
def add_comment(recipe_id):
    comment = request.get_json(force=True)
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    if user is None:
        return jsonify({"msg": "user not found"}), 404
    else:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        if recipe is None:
            return jsonify({"msg": "recipe not found"}), 404
        if comment["is_reply"]:
            og_comment_id = comment["original_comment_id"]
            og_comment = Comment.query.filter(Comment.id == og_comment_id).first()
            if og_comment is None:
                return jsonify({"msg": "original comment not found"}), 404
        if len(comment["text"]) == 0:
            return jsonify({"msg": "comment should not be empty"}), 404
        new_comment = Comment(
            **{
                "text": comment["text"],
                "commenter_id": user.id,
                "recipe_id": recipe_id,
                "is_reply": comment["is_reply"],
                "original_comment_id": comment["original_comment_id"],
            }
        )
        db.session.add(new_comment)
        db.session.commit()
        return Response(status=201)


@app.route("/api/recipes/<int:recipe_id>/comments")
def get_recipe_comments(recipe_id):
    r = getRecipeById(recipe_id)
    if r is None:
        abort(404)
    else:
        comments = getCommentsTreeForRecipe(r)
        return jsonify({"comments": comments})