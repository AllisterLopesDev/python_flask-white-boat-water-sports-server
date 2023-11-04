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
    vehical_order_info = db.session.query(VehicalOrder.id, VehicalOrder.vehical_id, VehicalOrder.order_id, VehicalOrder.commission_amount, VehicalOrder.payment_status)\
        .filter(VehicalOrder.id == (db.session.query(Order.id).filter(Order.serial_no == 'AWS1208').subquery())).first()

    result = {
        'id': vehical_order_info[0],
        'vehical_id': vehical_order_info[1],
        'order_id': vehical_order_info[2],
        'commission_amount': vehical_order_info[3],
        'payment_status': vehical_order_info[4]
    }
    return jsonify(result)

# delete a order api
@blue_print.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Your delete logic here
    return jsonify({'message': f'Deleted order with ID {order_id}'})