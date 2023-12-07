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
    Vehical_id = request.args.get('Vehical_id')
    contact_no = request.json.get('contact')

    try:
        # condition
        condition = VehicalOrder.vehical_id == Vehical_id
       # filter records based on condition
        records = VehicalOrder.query.filter(condition).all()
        temp = []
        vehical_order_data = []
        temp_vehical_id = 0
        # update selected records
        for record in records:
            record.payment_status=True
            temp.append({'id':record.id, 'order_id':record.order_id,'vehical':record.vehical_id,'commission_amount':record.commission_amount, 'payment_status':record.payment_status})
            
            temp_vehical_id = record.vehical_id
            filter_record_condition = Vehical.id == temp_vehical_id
            # filter record based on condition
            filter_vehical_data = Vehical.query.filter(filter_record_condition).all()
            for vehical in filter_vehical_data:
                vehical.contact = contact_no
                vehical_order_data.append({'id':vehical.id,'registration_no':vehical.registration_no,'name':vehical.name,'contact':vehical.contact,'created_at':vehical.created_at})


        db.session.commit()        
        return jsonify({
            'status':200,
            'message':'amount paid',
            'vehical_order_list':temp,
            'vehical_data':vehical_order_data
        }),200
    except Exception as e:
        db.session.rollback()
        return str(e),500  

# response ----- >  order_details, transport_name,'reg_no'
@blue_print.route("/get_unpaid_commission", methods=["GET"])
def getUnpaidCommission():
    v_no = request.args.get('Vehical_no')

    if not v_no:
        return {
            'status': 400,
            'message': 'vehical id required'
        }
    # query
    records = db.session.query(Vehical.id,Vehical.registration_no,Vehical.name, Order.serial_no, Order.created_at,Order.pax, Order.amount,VehicalOrder.commission_amount, VehicalOrder.payment_status).join(Vehical).join(Order).filter(Vehical.registration_no.like(f'%{v_no}')).filter(VehicalOrder.payment_status == 0).all()
    
    if not records:
        return {
            'status': 400,
            'message': 'no data available'
        }

    record_list  = []
    for record in records:
        record_list.append({'vehical_id':record.id,'vehical_no':record.registration_no,'transport_name': record.name,'serial_no': record.serial_no,'created_at':record.created_at , 'commission_payment_status': record.payment_status, 'pax': record.pax, 'commission':record.commission_amount})    

    return jsonify({'order_details': record_list
                    })
