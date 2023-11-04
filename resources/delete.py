from flask import Blueprint, jsonify, request
from sqlalchemy import func
from db import db

from models.order import Order
from models.vehical import Vehical
from models.vehical_order import VehicalOrder

blue_print = Blueprint("delete_data", __name__)

@blue_print.route('/get_order_details', methods=['GET'])
def orderDetails():
    ticket_no = request.args.get('serial_no')
    if not ticket_no:
        return jsonify({
                'success': False,
                'message': 'ticket_no required',
                'status': 400}), 400
    
    
    return

# delete a order api
@blue_print.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Your delete logic here
    return jsonify({'message': f'Deleted order with ID {order_id}'})