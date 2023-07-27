import random
import string
from flask import Blueprint, jsonify, request
from db import db
from models.order import Order
from models.vehical import Vehical
from models.vehical_order import VehicalOrder

blue_print = Blueprint("booking", __name__)

@blue_print.route("/booking", methods=["POST"])
def booking():
    pax = request.json.get('pax')
    amount = request.json.get('amount')
    commission = request.json.get('commission')
    reg_no = request.json.get('reg_no')
    name = request.json.get('name')
    contact = request.json.get('contact')

    if not pax or not amount or not reg_no or not name or not contact:
        return jsonify({
            'success': False,
            'message': 'All fields (pax, amount, reg_no, name, contact) are required',
            'status': 400
        }), 400

    # calculate commission
    if not commission:
        commission = (50 / 100) * amount
    else:
        commission = commission

    # Generate the serial number
    serial_number = random.randint(1000, 9999)


    # check if vehical already exist in database
    vehical_exist = Vehical.query.filter_by(registration_no=reg_no).first()

    if vehical_exist:
        order_details = Order(serial_no=serial_number, pax=pax, amount=amount)
        db.session.add(order_details)
        db.session.commit()

        vehical_order_data = VehicalOrder(vehical_id = vehical_exist.id,order_id = order_details.id, commission_amount = commission)
        db.session.add(vehical_order_data)
        db.session.commit()
    else:
        vehical_details = Vehical(registration_no=reg_no, name=name, contact=contact)
        order_details = Order(serial_no=serial_number, pax=pax, amount=amount)
    
        db.session.add(order_details)
        db.session.add(vehical_details)
        db.session.commit()

        vehical_order_data = VehicalOrder(vehical_id = vehical_details.id,order_id = order_details.id, commission_amount = commission)
        db.session.add(vehical_order_data)
        db.session.commit()

    

    response_data = {
        'success': True,
        'message': 'Booking done',
        'status': 200,
        'result': {
            'order': {
                'id': order_details.id,
                'serial_number': serial_number,
                'pax': pax,
                'amount': amount,
                'date': order_details.created_at.strftime('%Y-%m-%d')
            },
            'vehical': {
                'reg_no': reg_no,
                'name': name,
                'contact': contact
            },
            'vehical_order': {
                'id': vehical_order_data.id,
                'vehical_id': vehical_exist.id if vehical_exist else vehical_details.id,
                'order_id': vehical_order_data.order_id,
                'commission': vehical_order_data.commission_amount
            }
        }
    }

    return jsonify(response_data), 200





@blue_print.route("/private_booking", methods=["POST"])
def privateBooking():
    pax = request.json.get('pax')
    amount = request.json.get('amount')

    if not pax or not amount:
        return jsonify({
            'success': False,
            'message': 'fields (pax, amount) are required',
            'status': 400
        }), 400

    # Generate the serial number
    serial_number = random.randint(1000, 9999)

    order_details = Order(serial_no=serial_number, pax=pax, amount=amount)
    db.session.add(order_details)
    db.session.commit()


    vehical_order_data = VehicalOrder(order_id = order_details.id)
    db.session.add(vehical_order_data)
    db.session.commit()

    

    response_data = {
        'success': True,
        'message': 'private Booking done',
        'status': 200,
        'result': {
            'order': {
                'id': order_details.id,
                'serial_number': serial_number,
                'pax': pax,
                'amount': amount,
                'date': order_details.created_at.strftime('%Y-%m-%d')
            }
        }
    }

    return jsonify(response_data), 200