from flask import Blueprint, app, jsonify, request;

from db import db
from models.credential import Credential
from models.user import User

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
    if user:
        userExist = User.query.filter_by(credential_id=user.id).first()
        # user data
        user_data = {
        'credential_id':user.id,
        'email': user.email,
        'user_id': userExist.id,
        'first_name': userExist.first_name,
        'last_name': userExist.last_name,
        'contact': userExist.contact,
        'email': user.email,
        }
        

    # check if user credentials are valid
    if not user or not user.password:
        return {"status": "401",
                "message": "invalid email or password"}, 401

    

    # api response
    return {"status": "200",
            "message": "login successful",
            "user": user_data,
            }, 200
