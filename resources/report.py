from flask import Blueprint,Flask, request, jsonify
from db import db

blue_print = Blueprint("report", __name__)

# generate report api route
@blue_print.route("single_day_report", methods=["POST"])
def generateSingleDayReport():

    date = request.json.get("date")

    if not date:
        return {
            'status': 400,
            'message': 'date required'
        }, 400
    
    