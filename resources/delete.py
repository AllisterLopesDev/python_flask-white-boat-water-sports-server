from flask import Blueprint, jsonify, request
from sqlalchemy import func
from db import db

from models.order import Order
from models.vehical import Vehical
from models.vehical_order import VehicalOrder

blue_print = Blueprint("delete_data", __name__)

@blue_print.route('/get_order_details', methods=['GET'])
def orderDetails():
    serial_no = request.args.get('serial_no')
    if not serial_no:
        return jsonify({
                'success': False,
                'message': 'serial_no required',
                'status': 400}), 400
    
    order_exist = Order.query.filter_by(serial_no=serial_no).first()

    # if order_exist :
    #     print(Order.id)
    
    if not order_exist:
         return jsonify({
                'success': False,
                'message': 'record not found',
                'status': 400}), 400

    response = {
        'id': order_exist.id,
        'amount': order_exist.amount,
        'serial_no': order_exist.serial_no,
        'pax': order_exist.pax,
        'created_at': order_exist.created_at,
        'payment_method': order_exist.payment_method
    }

    return jsonify(response)



# delete a order api
@blue_print.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id): 

    order_exist = Order.query.get(order_id)
    if not order_exist:
        return jsonify({
        'success': False,
        'message': 'order not found',
        'status': 400
        }), 400

    vehical_order_exist = VehicalOrder.query.filter_by(order_id=order_id).first()
    if vehical_order_exist:
        db.session.delete(vehical_order_exist)
        vehical_id = vehical_order_exist.vehical_id
        vehical_exist = Vehical.query.filter_by(id=vehical_id).first()
        
        if vehical_exist:
            db.session.delete(vehical_exist)
    
    db.session.delete(order_exist)

    db.session.commit()

    return jsonify({'message': f'Deleted order with ID {order_id}'})