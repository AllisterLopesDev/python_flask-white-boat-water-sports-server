from flask import Blueprint, jsonify, request
from sqlalchemy import func
from db import db

from models.order import Order
from models.vehical import Vehical
from models.vehical_order import VehicalOrder

blue_print = Blueprint("delete_data", __name__)

# delete a order api

@blue_print.route("/delete_order", methods=["GET"])
def deleteOrderData():

    ticket_no = request.json.get('serial_no')

    if not ticket_no:
        return jsonify({
            'success': False,
            'message': 'ticket_no. is required',
            'status': 400
        }), 400
    
    
    # try:



        

    # except Exception as e:
    #     return jsonify({'error': 'An error occurred while generating the report.'}), 500

    return