from functools import wraps
from flask import request, jsonify, g

from firebase_admin import auth


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "No token found."
            }), 404

        try:
            token = auth_header.split("Bearer ")[1]

            decoded_token = auth.verify_id_token(token)

            # equivalent of req.user
            g.user = decoded_token

            return f(*args, **kwargs)

        except Exception as error:
            return jsonify({
                "message": "Invalid or expired token.",
                "error": str(error)
            }), 401

    return decorated_function