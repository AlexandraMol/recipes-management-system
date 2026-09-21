from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

from firebase.firebase_config import *

# importing routes
from routes.auth_routes import auth_routes
from routes.recipe_routes import recipe_routes
from routes.user_routes import user_routes

# generate mock data
from scripts.upload_data import upload_data_to_database

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = os.getenv("PORT", 5000)

# Register API routes
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(recipe_routes, url_prefix="/api/recipe")
app.register_blueprint(user_routes, url_prefix="/api/user")

@app.route("/")
def home():
    return {"message": "API running"}

@app.route("/uploadData", methods=["GET"])
def upload_data():
    upload_data_to_database()
    return {"message": "Data uploaded"}


if __name__ == "__main__":
    app.run(debug=True, port=int(PORT))