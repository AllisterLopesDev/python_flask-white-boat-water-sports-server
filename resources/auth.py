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
        ## user data
        user_data = {
        'id': userExist.id,
        'first_name': userExist.first_name,
        'last_name': userExist.last_name,
        'contact': userExist.contact,
        'role': userExist.role
        }
        credential_data = {
                'id':user.id,
                'email':user.email,
                'password':user.password,
                'initial_login':user.initial_login
            }
        if user.initial_login == 0:
            return {"status": "201",
            "message": "Password Change Required",
            "credential": credential_data,
            "user":user_data
            }, 200
        
        
        

    # check if user credentials are valid
    if not user or not user.password:
        return {"status": "401",
                "message": "invalid email or password"}, 401

    

    # api response
    return {"status": "200",
            "message": "login successful",
            "user": user_data,
            "credential":credential_data
            }, 200
