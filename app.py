from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy
from db import db

from models.user import User
from models.credential import Credential

app = Flask(__name__)

# CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/advanture_boat_trip'
db.init_app(app)
ma = Marshmallow(app)



@app.route('/',methods=['GET'])
def home():
    return 'WELCOME TO WHITE WATER ADVENTURE'





@app.route("/user", methods=["GET", "POST"])
def user():
    users = Credential.query.all()
    user_list = []
    for user in users:
        user_list.append({'id': user.id, 'email': user.email, 'password': user.password})
    return jsonify(user_list)







# user login route / user auth
@app.route("/login", methods=["POST"])
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







# INSERT DATA TO DATABASE / USER REGISTRATION
@app.route('/register-user', methods=['POST'])
def inserData():
    email = request.json.get('email')
    password = request.json.get('password')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    role = request.json.get('role')


    if role == 'admin':
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'email and password are required',
                'status': 400}), 400

        existing_user = Credential.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'email already exists.',
                'status': 410}), 410
        
        if not password:
            return jsonify({
                'success': False,
                'message': 'password required',
                'status': 400}), 400
        
        user_credential = Credential(email=email, password=password)
        db.session.add(user_credential)
        db.session.commit()
    else:

        if not email:
            return jsonify({
                'success': False,
                'message': 'email required',
                'status': 400}), 400

        existing_user = Credential.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'email already exists.',
                'status': 410}), 410
        
        user_credential = Credential(email=email)
        db.session.add(user_credential)
        db.session.commit()

    if not firstname:
        return jsonify({
            'success': False,
            'message': 'enter firstname',
            'status': 400
        }), 400
    
    if not lastname:
        return jsonify({
            'success': False,
            'message': 'enter lastname',
            'status': 400
        }), 400
    
    if not role:
        return jsonify({
            'success': False,
            'message': 'enter user role',
            'status': 400
        }), 400

    if not firstname or not lastname or not role:
            return jsonify({
                'success': False,
                'message': 'firstname , lastname and role are reqired',
                'status': 400}), 400
    else:
        user_details = User(first_name=firstname, last_name=lastname, role=role, credential_id=user_credential.id)
        db.session.add(user_details)
        db.session.commit()

    return jsonify({
        'success':True,
        'message': 'user added',
        'status': 200}), 200


if __name__ == '__main__':
    app.run(debug = True)