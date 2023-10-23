from flask import Blueprint, app, jsonify, request
from sqlalchemy import text
from db import db

from models.vehical_order import VehicalOrder
from models.order import Order
from models.vehical import Vehical

blue_print = Blueprint("commision", __name__)

@blue_print.route("/unpaid_commission", methods=["GET"])
def unpaidCommission():

    vehical_id=request.args.get('vehical_id')
    if not vehical_id:
        return {
            'status': 400,
            'message': 'vehical id required'
        }
    response_list = []
    total_commission_amount = 0

    # fetch all commission record based on vehical id  
    commission_records = VehicalOrder.query.filter_by(vehical_id=vehical_id).all()
                 # , payment_status=False
    for record in commission_records:
        order = Order.query.filter_by(id=record.order_id).first()
        order_obj = { 
            'pax':order.pax, 
            'amount':order.amount, 
            'payment_method':order.payment_method
        } 
        response_list.append({'id':record.id, 'order_id':record.order_id,'order':order_obj,'commission_amount':record.commission_amount, 'payment_status':record.payment_status})
        total_commission_amount = total_commission_amount + record.commission_amount

    # fetch vehical details
    vehical_data = Vehical.query.filter_by(id=vehical_id).first()
    vehical_details = {
        'id':vehical_data.id,
        'regno':vehical_data.registration_no,
        'name':vehical_data.name,
    }

    # store response data
    response_data = {
        'vehical_order':response_list,
        # 'order_list':Order_list,
        'vehical_details':vehical_details,
        'total_amount':total_commission_amount
    } 
   
    return jsonify(response_data)


@blue_print.route("/update_commisssion_payment_status", methods=["PUT"])
def updateCommissionPaymentStatus():
    Vehical_order_id = request.args.get('Vehical_order_id')
    order_id = request.args.get('order_id')
    Vehical_id = request.args.get('Vehical_id')

    try:
        # condition
        condition = VehicalOrder.vehical_id == Vehical_id
        # filter records based on condition
        records = VehicalOrder.query.filter(condition).all()
        temp = []
        # update selected records
        for record in records:
            record.payment_status=True
            temp.append({'id':record.id, 'order_id':record.order_id,'vehical':record.vehical_id,'commission_amount':record.commission_amount, 'payment_status':record.payment_status})
        db.session.commit()        
        return jsonify({
            'status':200,
            'message':'amount paid',
            'list':temp
        }),200
    except Exception as e:
        db.session.rollback()
        return str(e),500  

# response ----- >  order_details, transport_name,'reg_no'
@blue_print.route("/get_unpaid_commission", methods=["GET"])
def getUnpaidCommission():
    vehical_no = request.args.get('Vehical_no')

    # query
    records = db.session.query(Vehical.registration_no,Vehical.name, Order.serial_no, Order.created_at, VehicalOrder.payment_status). \
        join(Vehical).join(Order).filter(Vehical.registration_no.like(f'%{vehical_no}')).filter(VehicalOrder.payment_status == 0).all()
    
    record_list  = []
    for record in records:
        record_list.append({'serial_no': record.serial_no,'created_at':record.created_at , 'commission_payment_status': record.payment_status})    

    return jsonify({'order_details': record_list,
                    'transport_name': record.name,
                    'reg_no': record.registration_no
                    })
