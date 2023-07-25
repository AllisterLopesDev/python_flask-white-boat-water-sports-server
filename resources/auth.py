from flask import Blueprint, app, jsonify, request;

from db import db
from models.credential import Credential

blue_print = Blueprint("auth", __name__)

# user login route / user auth
@blue_print.route("/login", methods=["POST"])
def login():
    # empty data check
    email = request.json.get("email")
    password = request.json.get("password")
    if not email or not password:
        return {"status": "400",
                "message": "missing email or password"}, 400
    
    email = request.json.get("email")
    password = request.json.get("password")

    user = Credential.query.filter_by(email=email).first()

    # check if user credentials are valid
    if not user or not user.password:
        return {"status": "401",
                "message": "invalid email or password"}, 401

    # user data
    user_data = {
        'email': user.email,
    }

    # api response
    return {"status": "200",
            "message": "login successful",
            "user": user_data,
            }, 200
