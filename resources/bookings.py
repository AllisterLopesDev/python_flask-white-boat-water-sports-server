import random
import string
from flask import Blueprint, jsonify, request
from db import db
from models.order import Order
from models.vehical import Vehical
from models.vehical_order import VehicalOrder
from datetime import date

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
    discount_flag = request.json.get('discount_flag')

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
        if discount_flag:
            commission = pax * 100
        else:
            commission = pax * 150
    else:
        commission = commission

# get current date
    today = date.today()
    today_date = today.day
    today_month = today.month
    today_year = today.year % 100
    date_value = str(today_date)+str(today_month)+str(today_year)

    

    # Generate the serial number
    serial_initials = 'AWS' +date_value
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
                'payment-mode': payment_method,
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
    
    # get current date
    today = date.today()
    today_date = today.day
    today_month = today.month
    today_year = today.year % 100
    date_value = str(today_date)+str(today_month)+str(today_year)

    # Generate the serial number
    serial_initials = 'AWS'+date_value
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
                'payment-mode': payment_method,
                'amount': amount,
                'date': order_details.created_at.strftime('%Y-%m-%d')
            }
        }
    }

    return jsonify(response_data), 200



@blue_print.route("/get_all_orders",methods=["GET"])
def getAllOrderData():
    order_details =[]
    # vehical_order_details = {}
    # vehical_details = []
    records = Order.query.all()
    for record in records:
        order_data={'id':record.id,
                'serial_no':record.serial_no,
                'amount':record.amount,
                'pax':record.pax,
                'payment_method':record.payment_method}
        # check if orderid exist in vehical_order
        verhical_order_exist = VehicalOrder.query.filter_by(order_id=record.id).first()
        if verhical_order_exist:
            vehical_order_details = {
            'id':verhical_order_exist.id,
            'commission_amount':verhical_order_exist.commission_amount,
            'payment_status':verhical_order_exist.payment_status}
            
            # check if vehical_id exist in vehical
            vehical_exist = Vehical.query.filter_by(id=verhical_order_exist.vehical_id).first()
            if vehical_exist:
                vehical_details = {
                'id':vehical_exist.id,
                'vehical_name':vehical_exist.name,
                'reg_no':vehical_exist.registration_no,
                'created_at':vehical_exist.created_at  
                }
                order_details.append({'order_details':order_data,
                                    'vehical_order_data': vehical_order_details,
                                    'vehiacal_data': vehical_details})

        else:
            order_details.append({'order_details':order_data})  

    return jsonify(order_details)

@blue_print.route("/get_order_details_based_on_serial_no",methods=["GET"])
def getOrderData():
    # order_details =[]
    serial_no = request.args.get('serial_no')
    # vehical_order_details = {}
    # vehical_details = []
    record = Order.query.filter_by(serial_no=serial_no).first()
    if record:
        order_data={'id':record.id,
                'serial_no':record.serial_no,
                'amount':record.amount,
                'pax':record.pax,
                'payment_method':record.payment_method}
        # check if orderid exist in vehical_order
        verhical_order_exist = VehicalOrder.query.filter_by(order_id=record.id).first()
        if verhical_order_exist:
            vehical_order_details = {
            'id':verhical_order_exist.id,
            'commission_amount':verhical_order_exist.commission_amount,
            'payment_status':verhical_order_exist.payment_status}
            
            # check if vehical_id exist in vehical
            vehical_exist = Vehical.query.filter_by(id=verhical_order_exist.vehical_id).first()
            if vehical_exist:
                vehical_details = {
                'id':vehical_exist.id,
                'vehical_name':vehical_exist.name,
                'reg_no':vehical_exist.registration_no,
                'created_at':vehical_exist.created_at  
                }
                order_details = {'order_details':order_data,
                                    'vehical_order_data': vehical_order_details,
                                    'vehiacal_data': vehical_details}
                return jsonify(order_details)

        else:
            # order_details.append({'order_details':order_data})
            return jsonify({'order_details':order_data})        
    
    if not record:
        return jsonify({
            'success': False,
            'message': 'no order available with given Serial no.',
            'status': 400
        }), 400   
    
    # return jsonify(order_details)
    