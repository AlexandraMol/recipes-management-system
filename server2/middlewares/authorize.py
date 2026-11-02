from functools import wraps
from flask import request, jsonify, g
from firebase.firebase_config import db

from firebase_admin import auth


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Allow CORS preflight requests
        if request.method == "OPTIONS":
            return "", 204

        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "message": "Authentication required."
            }), 401

        token = auth_header[7:].strip()

        if not token:
            return jsonify({
                "message": "Authentication required."
            }), 401

        try:
            g.user = auth.verify_id_token(token)
        except Exception:
            return jsonify({
                "message": "Invalid or expired token."
            }), 401

        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        uid = g.user.get("uid") if getattr(g, "user", None) else None

        if not uid:
            return jsonify({
                "message": "Authentication required."
            }), 401

        user_doc = db.collection("users").document(uid).get()

        if not user_doc.exists:
            return jsonify({
                "message": "User not found."
            }), 403

        role = (user_doc.to_dict() or {}).get("role", "user")

        if role != "admin":
            return jsonify({
                "message": "Admin access required."
            }), 403

        return f(*args, **kwargs)

    return decorated_function