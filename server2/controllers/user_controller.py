from flask import jsonify, request, g
from firebase.firebase_config import db


def get_user_preferences():
    try:
        user = g.user
        uid = user.get("uid")

        user_doc = db.collection("users").document(uid).get()

        if not user_doc.exists:
            return jsonify({
                "data": {
                    "excludedIngredients": []
                }
            }), 200

        user_data = user_doc.to_dict()

        return jsonify({
            "data": {
                "excludedIngredients": user_data.get("excludedIngredients", [])
            }
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400


def update_user_preferences():
    try:
        user = g.user
        uid = user.get("uid")

        data = request.json
        excluded_ingredients = data.get("excludedIngredients", [])

        cleaned_ingredients = []

        for ingredient in excluded_ingredients:
            value = ingredient.strip().lower()

            if value and value not in cleaned_ingredients:
                cleaned_ingredients.append(value)

        db.collection("users").document(uid).update({
            "excludedIngredients": cleaned_ingredients
        })

        return jsonify({
            "message": "Preferences updated",
            "data": {
                "excludedIngredients": cleaned_ingredients
            }
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400

def get_current_user():
    uid = g.user["uid"]

    user_doc = db.collection("users").document(uid).get()

    if not user_doc.exists:
        return jsonify({
            "message": "User not found."
        }), 404

    user_data = user_doc.to_dict() or {}

    return jsonify({
        "uid": uid,
        "username": user_data.get("username"),
        "email": user_data.get("email"),
        "role": user_data.get("role", "user")
    }), 200