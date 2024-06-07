from datetime import datetime, timedelta, timezone
import json

from flask import jsonify, request, abort, Response
from flask_bcrypt import Bcrypt # type: ignore
from flask_jwt_extended import ( # type: ignore
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    set_access_cookies
)

from app import app, bcrypt, db
from app.controllers import (
    add_full_recipe,
    edit_recipe,
    add_new_user,
    get_recipe_by_id,
    get_recipe_tags,
    get_recipe_meta,
    get_recipe_ingredients,
    get_recipe_steps,
    get_recipe_full,
    get_comments_tree_for_recipe
)
from app.models import User, Recipe, Ingredient, Tag, Collection, Collection_Recipe, Comment


@app.route("/api/users", methods=["GET"])
def users():
    
    return jsonify([user.to_dict() for user in User.query.all()])

@app.route("/api/users/register", methods=["POST"])
def users_register():
    newUser = request.get_json(force=True)

    if User.query.filter(User.username == newUser["username"]).first():
        return jsonify(message="Username is already taken"), 400
    
    if User.query.filter(User.email == newUser["email"]).first():
        return jsonify(message="Email is already taken"), 400
    
    new_user = add_new_user(newUser)
    access_token = create_access_token(identity=new_user["username"])
    response = jsonify(data=new_user,
                       access_token=access_token,
                       msg='Register Successful')
    set_access_cookies(response, access_token)
    return response, 201
        

@app.route("/api/users/login", methods=["POST"])
def user_login():
    if request.json :
        username = request.json.get("username", None)
        password = request.json.get("password", None).encode("utf-8")
    user = User.query.filter(User.username == username).first()
    if user is not None and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        response = jsonify(access_token=access_token,
                           msg='Login Successful')
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({"msg": "Username or Password is incorrect"}), 401


@app.route("/api/user")
@jwt_required()
def user_profile():
    username = get_jwt_identity()
    print(username)
    return jsonify(User.query.filter(User.username == username).first().to_dict())


@app.route("/api/users/logout")
@jwt_required()
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
                    get_recipe_meta(recipe)
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
                    get_recipe_full(recipe)
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
                            "id": c.id,
                            "name": c.name,
                            "recipes": [get_recipe_meta(r) for r in c.recipes],
                        }
                        for c in user.collections
                    ]
                }
            )
        if request.method == "POST":
            if request.json:
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
                return jsonify(message="Collection has been created"), 201
            else:
                return jsonify(message="Collection already exist"), 400
        if request.method == "DELETE":
            if request.json:
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
                return jsonify(message="Collection has been deleted"), 200
            else:
                return jsonify(message="Collection doesn't exist"), 400


@app.route("/api/collections/<int:id>", methods=["GET", "POST", "DELETE"])
@jwt_required()
def user_collection(id):
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    collection = (
        Collection.query.filter(Collection.user_id == user.id)
        .filter(Collection.id == id)
        .first()
    )
    if user is None or collection is None:
        abort(404)
    if request.method == "GET":
        return jsonify(
            {"recipes": [get_recipe_meta(recipe) for recipe in collection.recipes]}
        )
    if request.method == "POST":
        if request.json:
            recipe_id = request.json.get("recipe_id", None)
        recipe = Recipe.query.get(recipe_id)
        if recipe is None:
            abort(404)
        else:
            if recipe.id in [r.id for r in collection.recipes]:
                return jsonify(msg='Recipe already in collection'), 200
            else:
                collection.recipes.append(recipe)
                db.session.commit()
                return jsonify(msg='Recipe added to collection'), 201
    if request.method == "DELETE":
        if request.json:
            recipe_id = request.json.get("recipe_id", None)
        recipe = Recipe.query.get(recipe_id)
        if recipe is None:
            abort(404)
        else:
            if recipe.id not in [r.id for r in collection.recipes]:
                return jsonify(msg='Recipe is not in collection'), 404
            else:
                db.session.query(Collection_Recipe).filter_by(
                    collection_id=collection.id
                ).filter_by(recipe_id=recipe_id).delete()
                db.session.commit()
                return jsonify(msg='Recipe has been removed from collection'), 204


@app.route("/api/recipes/create", methods=["POST"])
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
        new_recipe = add_full_recipe(newRecipeFull, user.id)
        return jsonify(msg=f'New Recipe created {new_recipe.name}, id {new_recipe.id}'), 201


@app.route("/api/recipes/<int:num>", methods=["GET"])
def recipes_n(num):
    r = get_recipe_by_id(num)
    if r is None:
        abort(404)
    else:
        return jsonify(get_recipe_meta(r))


@app.route("/api/recipes/<int:num>", methods=["PATCH", "DELETE"])
@jwt_required()
def recipes_n_path_delete(num):
    r = get_recipe_by_id(num)
    print(r)
    username = get_jwt_identity()
    print(username)
    user = User.query.filter(User.username == username).first()
    if r is None or user is None or user.username != r.contributor.username:
        abort(404)
    else:
        if request.method == "PATCH":
            newRecipeFull = request.get_json(force=True)
            edit_recipe(newRecipeFull, r, user)
            return Response(status=200)
        if request.method == "DELETE":
            db.session.delete(r)
            db.session.commit()
            return Response(status=200)


@app.route("/api/recipes/<int:num>/tags")
def recipes_n_tags(num):
    r = get_recipe_by_id(num)
    if r is None:
        abort(404)
    else:
        return jsonify({"tags": get_recipe_tags(r)})


@app.route("/api/recipes/<int:num>/ingredients")
def recipes_n_ingredients(num):
    r = get_recipe_by_id(num)
    if r is None:
        abort(404)
    else:
        return jsonify({"name": r.name, "recipe_ingredients": get_recipe_ingredients(r)})


@app.route("/api/recipes/<int:num>/steps")
def recipes_n_steps(num):
    r = get_recipe_by_id(num)
    if r is None:
        abort(404)
    else:
        return jsonify({"name": r.name, "recipe_steps": get_recipe_steps(r)})


@app.route("/api/recipes/<int:num>/full", methods=['GET'])
def recipes_n_full(num):
    r = get_recipe_by_id(num)
    if r is None:
        abort(404)
    else:
        return jsonify(get_recipe_full(r)), 200


@app.route("/api/recipes/count")
def recipes_count():
    return jsonify({"count": len(Recipe.query.all())})


@app.route("/api/recipes/all")
def recipes_all():
    return jsonify(
        {"recipes": [get_recipe_meta(recipe) for recipe in Recipe.query.all()]}
    )


@app.route("/api/recipes/bytag/<tag>")
def recipes_bytag(tag):
    return jsonify(
        {
            "recipes": [
                get_recipe_meta(r)
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
    r = get_recipe_by_id(recipe_id)
    if r is None:
        abort(404)
    else:
        comments = get_comments_tree_for_recipe(r)
        return jsonify({"comments": comments})