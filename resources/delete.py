from flask import Blueprint, jsonify, request
from sqlalchemy import func
from db import db

from models.order import Order
from models.vehical import Vehical
from models.vehical_order import VehicalOrder

blue_print = Blueprint("delete_data", __name__)

# delete a order api

@blue_print.route("/delete_order/<string:serial_no>", methods=["GET"])
def deleteOrderData(serial_no):

    ticket_no = request.json.get(serial_no)
    # initialize variable
    order_id = 0

    if not ticket_no:
        return jsonify({
            'success': False,
            'message': 'ticket_no. is required',
            'status': 400
        }), 400
    
    order_record = Order.query.filter_by(serial_no=serial_no).first()
    if order_record is not None:
        order_id = order_record.id

    
    
    # try:



        

    # except Exception as e:
    #     return jsonify({'error': 'An error occurred while generating the report.'}), 500

    return jsonify({
        'order_id': order_id,
        }), 200