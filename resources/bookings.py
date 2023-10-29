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
    booking_date = request.json.get('order_dateTime')
    # contact = request.json.get('contact')
    payment_method = request.json.get('payment_method')

    if not pax or not amount or not reg_no:
        return jsonify({
            'success': False,
            'message': 'All fields (pax, amount, reg_no) are required',
            'status': 400
        }), 400
    
    if not payment_method or not booking_date:
        return jsonify({
            'success': False,
            'message': 'fields (payment method, creation date) are required',
            'status': 400
        }), 400

    # calculate commission
    if not commission:
        commission = (50 / 100) * amount
    else:
        commission = commission

    # Generate the serial number
    serial_initials = 'AWS'
    serial_number =serial_initials + str(random.randint(1000, 9999))

    # check if serial no exist in database
    serial_number_exist = Order.query.filter_by(serial_no=serial_number).all
    if serial_number_exist:
        serial_number =serial_initials + str(random.randint(1000, 9999))

        vehical_details = Vehical(registration_no=reg_no, name=name)
        order_details = Order(serial_no=serial_number, pax=pax, amount=amount, payment_method=payment_method, created_at = booking_date)
    
        db.session.add(order_details)
        db.session.add(vehical_details)
        db.session.commit()

        vehical_order_data = VehicalOrder(vehical_id = vehical_details.id,order_id = order_details.id, commission_amount = commission)
        db.session.add(vehical_order_data)
        db.session.commit()

    #  response
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
                'name': name
            },
            'vehical_order': {
                'id': vehical_order_data.id,
                'vehical_id': vehical_details.id,
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
    payment_method = request.json.get('payment_method')
    booking_date = request.json.get('order_dateTime')

    if not pax or not amount or not payment_method or not booking_date:
        return jsonify({
            'success': False,
            'message': 'fields (pax, amount, payment method, creation date) are required',
            'status': 400
        }), 400

    # Generate the serial number
    serial_initials = 'AWS'
    serial_number = serial_initials + str(random.randint(1000, 9999))

    order_details = Order(serial_no=serial_number, pax=pax, amount=amount, payment_method=payment_method, created_at = booking_date)
    db.session.add(order_details)
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



@blue_print.route("/get_order_data",methods=["GET"])
def getOrderData():
    order_list =[]
    records = Order.query.all()
    for record in records:
        order_list.append({'id':record.id,'serial_no':record.serial_no,'amount':record.amount,'pax':record.pax,'payment_method':record.payment_method})
    return jsonify({
        'message':'success',
        'list':order_list
    })