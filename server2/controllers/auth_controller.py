from flask import request, jsonify
from firebase.firebase_config import db, firebase_auth
from datetime import datetime


def register():

    data = request.json

    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    try:

        # Username validation
        username_validation = (
            db.collection("users")
            .where("username", "==", username)
            .get()
        )

        if len(username_validation) > 0:
            return jsonify({
                "error": "This username is taken."
            }), 400

        # Email validation
        try:
            firebase_auth.get_user_by_email(email)

            return jsonify({
                "error": "An account with this email already exists."
            }), 400

        except:
            pass

        # Create Firebase user
        user = firebase_auth.create_user(
            email=email,
            password=password,
            display_name=username
        )

        # Save user in Firestore
        db.collection("users").document(user.uid).set({
            "username": username,
            "email": email,
            "createdAt": datetime.utcnow().isoformat()
        })

        return jsonify({
            "message": "User registered successfully!"
        }), 201

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400