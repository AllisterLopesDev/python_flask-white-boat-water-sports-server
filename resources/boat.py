from flask import Blueprint, app, jsonify, request;
from db import db
from models.boat import Boat
from models.user import User


blue_print = Blueprint("boat", __name__)

# add boat details
@blue_print.route("/add_boat_details", methods=["POST"])
def addBoatDetails():

    boat_reg_no = request.json.get("registration_no")
    capacity = request.json.get("capacity")
    user_id = request.json.get("user_id")

    if not boat_reg_no:
        return {"status": 400,
                "message": "ENTER reg.no"}, 400
    if not capacity:
        return {"status": 400,
                "message": "ENTER capacity"}, 400
    if not user_id:
        return {"status": 400,
                "message": "ENTER userid"}, 400
    
    # check if boat exist or not
    boat_exist = Boat.query.filter_by(registration_no = boat_reg_no).first()
    if boat_exist:
        return jsonify({
            'success': False,
            'message': 'Boat already exists.',
            'status': 410}), 410
    
    # check if the given userid is owner or admin and if admin that dont register the boat
    user_as_admin_exist = User.query.filter_by(id=user_id).first()
    if user_as_admin_exist.role == 'admin':
        return jsonify({
            'success': False,
            'message': 'ENTERED user_id belongs to admin',
            'status': 410}), 410

    boat_details = Boat(registration_no = boat_reg_no, capacity = capacity, user_id = user_id)
    db.session.add(boat_details)
    db.session.commit()

    # api response
    return {"status": "200",
            "message": "Boat added"
            }, 200


# get all available boats
@blue_print.route("/get_all_boats",methods=["GET"])
def getAllAvailableBoats():
    boats = Boat.query.all()
    boat_list = []
    for boat in boats:
        boat_list.append({'id': boat.id, 'reg_no': boat.registration_no, 'capacity': boat.capacity})
    return jsonify(boat_list)




# get boat owner details based on boat reg no
@blue_print.route("/boat_owner", methods=["GET"])
def getBoatOwners():
    boatreg_no = request.args.get("reg_no")

    try:
        user_boat_info = db.session.query(
            User.credential_id.label('cred_id'),
            User.first_name.label('fname'),
            User.last_name.label('lname'),
            User.address.label('address'),
            User.conatct.label('contact'),
            User.gender.label('gender'),
            User.id.label('userid'),
            Boat.registration_no.label('reg'),
            Boat.id.label('boatid')
        ).join(Boat, User.id == Boat.user_id).filter(Boat.registration_no.like(boatreg_no)).all()

        result = [
            {
                'credential_id': cred_id,
                'firstname': fname,
                'lastname': lname,
                'address': address,
                'contact': contact,
                'gender': gender,
                'userid': userid,
                'reg': reg,
                'boatid': boatid
            }
            for cred_id,fname,lname,address,contact,gender,userid,reg,boatid in user_boat_info
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while retrieving user boat info.'}), 500
    

# get number of boats and details OWNED BY A PARTICULAR OWNER
@blue_print.route("/boat_owned_by_owner", methods=["GET"])
def getOwnedBoats():
    uid = request.args.get("userid")

    # check if the given userid is owner or admin and if admin that dont register the boat
    user_as_admin_exist = User.query.filter_by(id=uid).first()
    if user_as_admin_exist.role == 'admin':
        return jsonify({
            'success': False,
            'message': 'ENTERED user_id belongs to admin',
            'status': 410}), 410

    try:
        user_boat_info = db.session.query(
            User.credential_id.label('cred_id'),
            User.first_name.label('fname'),
            User.last_name.label('lname'),
            User.id.label('userid'),
            Boat.registration_no.label('reg'),
            Boat.id.label('boatid')
        ).join(Boat, User.id == Boat.user_id).filter(User.id.like(uid)).all()

        result = [
            {
                'credential_id': cred_id,
                'firstname': fname,
                'lastname': lname,
                'userid': userid,
                'reg': reg,
                'boatid': boatid
            }
            for cred_id,fname,lname,userid,reg,boatid in user_boat_info
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while retrieving user boat info.'}), 500