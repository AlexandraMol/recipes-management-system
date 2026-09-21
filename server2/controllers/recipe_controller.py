from urllib.parse import unquote
from flask import request, jsonify
from firebase.firebase_config import db, storage
from google.cloud.firestore import Query
from utils.convertors import convert_from_base, convert_to_base
from datetime import datetime

def add_recipe():

    data = request.json

    username = data.get("username")
    name = data.get("name")

    try:

        validation = (
            db.collection("recipes")
            .where("name", "==", name)
            .where("username", "==", username)
            .get()
        )

        if len(validation) > 0:
            return jsonify({
                "error": "This recipe already exists."
            }), 400

        db.collection("recipes").add(data)

        return jsonify({
            "message": "Recipe added!"
        }), 201

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400
    
def get_user_recipes(username):

    try:

        user_recipes = (
            db.collection("recipes")
            .where("username", "==", username)
            .get()
        )

        recipes = [
            {
                "id": doc.id,
                **doc.to_dict()
            }
            for doc in user_recipes
        ]

        return jsonify({
            "data": recipes
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400
    
def get_other_user_recipes(username):

    try:

        recipes_snapshot = (
            db.collection("recipes")
            .where("visibility", "==", "Public")
            .get()
        )

        recipes = []

        for doc in recipes_snapshot:

            recipe = doc.to_dict()

            if recipe.get("username") != username:
                recipes.append({
                    "id": doc.id,
                    **recipe
                })

        return jsonify({
            "data": recipes
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400
    
def get_recipe_by_id(id):

    try:

        recipe = (
            db.collection("recipes")
            .document(id)
            .get()
        )

        if not recipe.exists:
            return jsonify({
                "message": "Recipe not found"
            }), 404

        return jsonify({
            "data": recipe.to_dict()
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400
    
def remove_recipe(id):
    try:
        recipe_ref = db.collection("recipes").document(id)
        recipe = recipe_ref.get()

        if not recipe.exists:
            return jsonify({
                "message": "Recipe not found"
            }), 404

        recipe_data = recipe.to_dict()
        image_url = recipe_data.get("imageUrl")

        if image_url:
            try:
                image_path = unquote(
                    image_url.split("/o/")[1].split("?")[0]
                )

                bucket = storage.bucket()
                blob = bucket.blob(image_path)

                if blob.exists():
                    blob.delete()

            except Exception as storage_error:
                print("Storage delete error:", str(storage_error))

        recipe_ref.delete()

        return jsonify({
            "message": "Recipe deleted"
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400
    
def edit_recipe(id):

    try:

        recipe_ref = (
            db.collection("recipes")
            .document(id)
        )

        recipe = recipe_ref.get()

        if not recipe.exists:
            return jsonify({
                "message": "Recipe not found"
            }), 404

        recipe_ref.update(request.json)

        return jsonify({
            "message": "Recipe updated"
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400

def generate_shopping_list():
    try:
        data = request.json
        recipe_ids = data.get("recipeIds")

        if not recipe_ids:
            return jsonify({"message": "Missing recipes"}), 400

        ingredients_to_buy = {}

        for recipe_id in recipe_ids:
            recipe = db.collection("recipes").document(recipe_id).get()

            if not recipe.exists:
                continue

            ingredients = recipe.to_dict().get("ingredients", [])

            for ingredient in ingredients:
                name = ingredient.get("name", "").lower().strip()
                unit = ingredient.get("unit", "").lower().strip()

                if not name or not unit:
                    continue

                try:
                    quantity = float(ingredient.get("quantity", 0))
                except:
                    quantity = 0

                quantity, base_unit = convert_to_base(quantity, unit)

                key = f"{name}_{base_unit}"

                if key in ingredients_to_buy:
                    ingredients_to_buy[key]["quantity"] += quantity
                else:
                    ingredients_to_buy[key] = {
                        "name": name,
                        "quantity": quantity,
                        "unit": base_unit
                    }

        shopping_list = []

        for item in ingredients_to_buy.values():
            quantity, unit = convert_from_base(
                item["quantity"],
                item["unit"]
            )

            shopping_list.append({
                "name": item["name"],
                "quantity": round(quantity, 2),
                "unit": unit
            })

        return jsonify({"data": shopping_list}), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 400
    
def search_recipes():
    try:
        data = request.json

        search_text = data.get("searchText", "").lower().strip()
        included_ingredients = [
            item.lower().strip()
            for item in data.get("includedIngredients", [])
            if item.strip()
        ]

        excluded_ingredients = [
            item.lower().strip()
            for item in data.get("excludedIngredients", [])
            if item.strip()
        ]

        categories = data.get("categories", [])
        difficulties = data.get("difficulties", [])
        max_preparation_time = data.get("maxPreparationTime")

        recipes_snapshot = (
            db.collection("recipes")
            .where("visibility", "==", "Public")
            .get()
        )

        results = []

        for doc in recipes_snapshot:
            recipe = doc.to_dict()

            recipe_name = recipe.get("name", "").lower()
            recipe_category = recipe.get("category", [])
            recipe_difficulty = recipe.get("difficulty", "")
            recipe_time = int(recipe.get("preparationTime", 0))

            ingredients = recipe.get("ingredients", [])
            ingredient_names = [
                ingredient.get("name", "").lower().strip()
                for ingredient in ingredients
            ]

            # 1. Search by recipe name
            if search_text and search_text not in recipe_name:
                continue

            # 2. Must contain selected ingredients
            if included_ingredients:
                if not all(
                    ingredient in ingredient_names
                    for ingredient in included_ingredients
                ):
                    continue

            # 3. Must NOT contain excluded ingredients
            if excluded_ingredients:
                if any(
                    excluded in ingredient_names
                    for excluded in excluded_ingredients
                ):
                    continue

            # 4. Category filter
            if categories:
                if not any(category in recipe_category for category in categories):
                    continue

            # 5. Difficulty filter
            if difficulties:
                if recipe_difficulty not in difficulties:
                    continue

            # 6. Preparation time filter
            if max_preparation_time:
                if recipe_time > int(max_preparation_time):
                    continue

            results.append({
                "id": doc.id,
                **recipe
            })

        return jsonify({"data": results}), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 400

def get_recently_viewed_recipes(username):
    try:
        history_snapshot = (
            db.collection("viewHistory")
            .where("username", "==", username)
            .where("interactionType", "==", "view")
            .order_by("timestamp", direction=Query.DESCENDING)
            .limit(8)
            .get()
        )

        recently_viewed = []

        for history_doc in history_snapshot:
            history_data = history_doc.to_dict()
            recipe_id = history_data.get("recipeId")

            if not recipe_id:
                continue

            recipe = db.collection("recipes").document(recipe_id).get()

            if not recipe.exists:
                continue

            recently_viewed.append({
                "id": recipe.id,
                **recipe.to_dict(),
                "viewedAt": history_data.get("viewedAt")
            })

        return jsonify({"data": recently_viewed}), 200

    except Exception as error:
        print("Recently viewed GET error:", str(error))

        return jsonify({
            "error": str(error)
        }), 400
    
def save_user_interaction():
    try:
        data = request.json

        username = data.get("username")
        recipe_id = data.get("recipeId")
        interaction_type = data.get("interactionType")
        search_query = data.get("searchQuery")

        if not username or not interaction_type:
            return jsonify({
                "message": "Missing username or interactionType"
            }), 400

        timestamp = datetime.utcnow().isoformat()

        if interaction_type == "view":
            if not recipe_id:
                return jsonify({"message": "Missing recipeId"}), 400

            recipe = db.collection("recipes").document(recipe_id).get()

            if not recipe.exists:
                return jsonify({"message": "Recipe not found"}), 404

            recipe_data = recipe.to_dict()

            if recipe_data.get("username") == username:
                return jsonify({"message": "Own recipe view ignored"}), 200

            doc_id = f"{username}_{recipe_id}_view"

        elif interaction_type in ["favorite", "rating"]:
            if not recipe_id:
                return jsonify({"message": "Missing recipeId"}), 400

            doc_id = f"{username}_{recipe_id}_{interaction_type}"

        elif interaction_type == "search":
            if not search_query:
                return jsonify({"message": "Missing searchQuery"}), 400

            doc_id = f"{username}_search_{int(datetime.utcnow().timestamp())}"

        else:
            return jsonify({"message": "Invalid interaction type"}), 400

        db.collection("viewHistory").document(doc_id).set({
            "username": username,
            "recipeId": recipe_id,
            "interactionType": interaction_type,
            "searchQuery": search_query,
            "timestamp": timestamp,
            "viewedAt": timestamp if interaction_type == "view" else None
        })

        return jsonify({
            "message": "Interaction saved"
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400
    
def toggle_favorite_recipe(recipe_id):
    try:
        data = request.json
        username = data.get("username")

        if not username:
            return jsonify({"message": "Missing username"}), 400

        recipe = db.collection("recipes").document(recipe_id).get()

        if not recipe.exists:
            return jsonify({"message": "Recipe not found"}), 404

        favorite_id = f"{username}_{recipe_id}"
        favorite_ref = db.collection("favorites").document(favorite_id)
        favorite = favorite_ref.get()

        if favorite.exists:
            favorite_ref.delete()
            is_favorite = False
            message = "Recipe removed from favorites"
        else:
            favorite_ref.set({
                "username": username,
                "recipeId": recipe_id,
                "createdAt": datetime.utcnow().isoformat()
            })

            db.collection("viewHistory").document(
                f"{username}_{recipe_id}_favorite"
            ).set({
                "username": username,
                "recipeId": recipe_id,
                "interactionType": "favorite",
                "timestamp": datetime.utcnow().isoformat(),
                "searchQuery": None
            })

            is_favorite = True
            message = "Recipe added to favorites"

        return jsonify({
            "message": message,
            "isFavorite": is_favorite
        }), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 400
    
def rate_recipe(recipe_id):
    try:
        data = request.json

        username = data.get("username")
        rating_value = data.get("rating")

        if not username or rating_value is None:
            return jsonify({"message": "Missing username or rating"}), 400

        rating_value = int(rating_value)

        if rating_value < 1 or rating_value > 5:
            return jsonify({"message": "Rating must be between 1 and 5"}), 400

        recipe_ref = db.collection("recipes").document(recipe_id)
        recipe = recipe_ref.get()

        if not recipe.exists:
            return jsonify({"message": "Recipe not found"}), 404

        rating_id = f"{username}_{recipe_id}"

        db.collection("ratings").document(rating_id).set({
            "username": username,
            "recipeId": recipe_id,
            "rating": rating_value,
            "createdAt": datetime.utcnow().isoformat()
        })

        ratings_snapshot = (
            db.collection("ratings")
            .where("recipeId", "==", recipe_id)
            .get()
        )

        ratings = [
            doc.to_dict().get("rating", 0)
            for doc in ratings_snapshot
        ]

        number_of_ratings = len(ratings)
        average_rating = (
            sum(ratings) / number_of_ratings
            if number_of_ratings > 0
            else 0
        )

        recipe_ref.update({
            "averageRating": round(average_rating, 2),
            "numberOfRatings": number_of_ratings
        })

        db.collection("viewHistory").document(
            f"{username}_{recipe_id}_rating"
        ).set({
            "username": username,
            "recipeId": recipe_id,
            "interactionType": "rating",
            "timestamp": datetime.utcnow().isoformat(),
            "searchQuery": None
        })

        return jsonify({
            "message": "Rating saved",
            "averageRating": round(average_rating, 2),
            "numberOfRatings": number_of_ratings
        }), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 400

def get_recipe_status(recipe_id, username):
    try:
        favorite_id = f"{username}_{recipe_id}"
        rating_id = f"{username}_{recipe_id}"

        favorite_doc = (
            db.collection("favorites")
            .document(favorite_id)
            .get()
        )

        rating_doc = (
            db.collection("ratings")
            .document(rating_id)
            .get()
        )

        user_rating = 0

        if rating_doc.exists:
            user_rating = rating_doc.to_dict().get("rating", 0)

        return jsonify({
            "isFavorite": favorite_doc.exists,
            "userRating": user_rating
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400
    
def get_favorite_recipes(username):
    try:
        favorites_snapshot = (
            db.collection("favorites")
            .where("username", "==", username)
            .get()
        )

        favorite_recipes = []

        for favorite_doc in favorites_snapshot:
            favorite_data = favorite_doc.to_dict()
            recipe_id = favorite_data.get("recipeId")

            if not recipe_id:
                continue

            recipe = db.collection("recipes").document(recipe_id).get()

            if not recipe.exists:
                continue

            recipe_data = recipe.to_dict()

            favorite_recipes.append({
                "id": recipe.id,
                **recipe_data,
                "favoritedAt": favorite_data.get("createdAt")
            })

        return jsonify({
            "data": favorite_recipes
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400