from flask import Blueprint, app, jsonify, request;
from db import db
from models.boat import Boat


blue_print = Blueprint("boat", __name__)

# add boat details
@blue_print.route("/add_boat_details", methods=["POST"])
def addBoatDetails():

    boat_reg_no = request.json.get("registration_no")
    capacity = request.json.get("capacity")
    user_id = request.json.get("user_id")

    if not boat_reg_no:
        return {"status": "400",
                "message": "ENTER reg.no"}, 400
    if not capacity:
        return {"status": "400",
                "message": "ENTER capacity"}, 400
    if not user_id:
        return {"status": "400",
                "message": "ENTER userid"}, 400
    
    # check if boat exist or not
    boat_exist = Boat.query.filter_by(registration_no = boat_reg_no).first()
    if boat_exist:
        return jsonify({
            'success': False,
            'message': 'Boat already exists.',
            'status': 410}), 410
    

    boat_details = Boat(registration_no = boat_reg_no, capacity = capacity, user_id = user_id)
    db.session.add(boat_details)
    db.session.commit()

    # api response
    return {"status": "200",
            "message": "Boat added"
            }, 200