from flask import Blueprint
from controllers.recipe_controller import (
    add_recipe,
    edit_recipe,
    remove_recipe,
    get_recipe_by_id,
    get_user_recipes,
    get_other_user_recipes,
    generate_shopping_list,
    search_recipes,
    get_recently_viewed_recipes,
    save_user_interaction,
    toggle_favorite_recipe,
    rate_recipe,
    get_recipe_status,
    get_favorite_recipes
)

from middlewares.authorize import authorize

recipe_routes = Blueprint("recipe_routes", __name__)


@recipe_routes.route("/add", methods=["POST"])
@authorize
def add():
    return add_recipe()


@recipe_routes.route("/edit/<id>", methods=["PUT"])
@authorize
def edit(id):
    return edit_recipe(id)


@recipe_routes.route("/remove/<id>", methods=["DELETE"])
@authorize
def remove(id):
    return remove_recipe(id)


@recipe_routes.route("/recipe/<id>", methods=["GET"])
@authorize
def get_recipe(id):
    return get_recipe_by_id(id)

@recipe_routes.route("/recently-viewed/<username>", methods=["GET"])
@authorize
def recently_viewed(username):
    return get_recently_viewed_recipes(username)

@recipe_routes.route("/interaction", methods=["POST"])
@authorize
def interaction():
    return save_user_interaction()

@recipe_routes.route("/favorites/<username>", methods=["GET"])
@authorize
def favorite_recipes(username):
    return get_favorite_recipes(username)

@recipe_routes.route("/<username>", methods=["GET"])
@authorize
def get_recipes(username):
    return get_user_recipes(username)


@recipe_routes.route("/otherRecipes/<username>", methods=["GET"])
@authorize
def get_other_recipes(username):
    return get_other_user_recipes(username)


@recipe_routes.route("/shopping-list", methods=["POST"])
@authorize
def shopping_list():
    return generate_shopping_list()

@recipe_routes.route("/search", methods=["POST"])
@authorize
def search():
    return search_recipes()

@recipe_routes.route("/favorite/<recipe_id>", methods=["POST"])
@authorize
def favorite(recipe_id):
    return toggle_favorite_recipe(recipe_id)


@recipe_routes.route("/rating/<recipe_id>", methods=["POST"])
@authorize
def rating(recipe_id):
    return rate_recipe(recipe_id)

@recipe_routes.route("/status/<recipe_id>/<username>", methods=["GET"])
@authorize
def recipe_status(recipe_id, username):
    return get_recipe_status(recipe_id, username)
