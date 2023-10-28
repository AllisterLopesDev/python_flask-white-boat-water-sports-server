from flask import Blueprint, app, jsonify, request
from models.vehical import Vehical

blue_print = Blueprint("vehicals", __name__)

# GET ALL VEHICALS
@blue_print.route("/vehical_list", methods=["GET", "POST"])
def vehicalList():
    vehicals = Vehical.query.all()
    vehical_list = []
    for v in vehicals:
        vehical_list.append({'id': v.id, 'name': v.name, 'reg_no': v.registration_no})
    return jsonify(vehical_list)