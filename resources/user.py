from flask import Blueprint, app, jsonify, request

from models.credential import Credential
from db import db
from models.user import User


blue_print = Blueprint("user", __name__)



# GET ALL AVAILABLE USERS

@blue_print.route("/user", methods=["GET", "POST"])
def user():
    users = Credential.query.all()
    user_list = []
    for user in users:
        user_list.append({'id': user.id, 'email': user.email, 'password': user.password})
    return jsonify(user_list)





# INSERT DATA TO DATABASE / USER REGISTRATION
@blue_print.route('/register-user', methods=['POST'])
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