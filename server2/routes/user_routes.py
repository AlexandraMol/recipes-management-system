from flask import Blueprint
from controllers.user_controller import (
    get_user_preferences,
    update_user_preferences
)
from middlewares.authorize import authorize

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/preferences", methods=["GET"])
@authorize
def preferences():
    return get_user_preferences()


@user_routes.route("/preferences", methods=["PUT"])
@authorize
def update_preferences():
    return update_user_preferences()