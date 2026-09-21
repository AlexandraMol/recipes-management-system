from firebase.firebase_config import db, firebase_auth
from scripts.generate_recipes import add_recipes
from scripts.generate_users import add_user


def upload_data_to_database():
    try:
        users = add_user(5)

        if not users:
            print("No users generated")
            return

        recipes_ref = db.collection("recipes")

        for user in users:
            user_auth = firebase_auth.create_user(
                email=user["email"],
                password=user["password"],
                display_name=user["username"]
            )

            db.collection("users").document(user_auth.uid).set({
                "username": user["username"],
                "email": user["email"],
                "createdAt": user["createdAt"]
            })

            recipes = add_recipes(5, user["username"])

            if not recipes:
                print("No recipes generated")
                continue

            batch = db.batch()

            for recipe in recipes:
                recipe_ref = recipes_ref.document()
                batch.set(recipe_ref, recipe)

            batch.commit()

        print("Data uploaded successfully")

    except Exception as error:
        print(str(error))