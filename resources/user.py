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


# GET ALL AVAILABLE owners
@blue_print.route("/user_as_owner", methods=["GET", "POST"])
def owner():
    owners = User.query.filter(User.role.like('%owner%'))
    owner_list = []
    for user in owners:
        owner_list.append({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,'address': user.address, 'contact': user.contact, 'gender': user.gender, 'credential_id':user.credential_id})
    return jsonify(owner_list)




# INSERT DATA TO DATABASE / USER REGISTRATION
@blue_print.route('/register-user', methods=['POST'])
def inserData():
    email = request.json.get('email')
    password = request.json.get('password')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    address = request.json.get('address')
    contact = request.json.get('contact')
    gender = request.json.get('gender')
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
    
    if not address:
        return jsonify({
            'success': False,
            'message': 'enter address',
            'status': 400
        }), 400
    
    if not contact:
        return jsonify({
            'success': False,
            'message': 'enter contact',
            'status': 400
        }), 400
    
    if not gender:
        return jsonify({
            'success': False,
            'message': 'enter gender',
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
        user_details = User(first_name=firstname, last_name=lastname, role=role, address=address, contact=contact, gender=gender, credential_id=user_credential.id)
        db.session.add(user_details)
        db.session.commit()

    return jsonify({
        'success':True,
        'message': 'user added',
        'status': 200}), 200