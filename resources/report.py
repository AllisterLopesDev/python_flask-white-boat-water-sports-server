from flask import Blueprint, jsonify, request
from sqlalchemy import func, and_
from db import db
from models.order import Order
from models.vehical_order import VehicalOrder

blue_print = Blueprint("report", __name__)

# route to get report of all orders
@blue_print.route("/get_overall_report", methods=["GET"])
def generateOverallReport():
    try:
        order_summary = db.session.query(
            func.date(Order.created_at).label('order_date'),
            func.sum(Order.pax).label('pax'),
            func.sum(Order.amount).label('total_amount'),
            func.sum(VehicalOrder.commission_amount).label('commission')
        ).join(VehicalOrder, Order.id == VehicalOrder.order_id).group_by(func.date(Order.created_at)).all()

        result = [
            {
                'order_date': order_date.strftime('%Y-%m-%d'),
                'pax':pax,
                'total_amount': total_amount,
                'commission': commission
            }
            for order_date,pax, total_amount, commission in order_summary
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while generating the report.'}), 500
    


# route to get report based on a given date
@blue_print.route("/get_single_day_report", methods=["GET"])
def generateReportBasedOnDate():

    date = request.args.get('date')
    if not date:
        return {
            'status': 400,
            'message': 'date required'
        }

    try:
        order_summary = db.session.query(
            func.date(Order.created_at).label('order_date'),
            func.sum(Order.pax).label('pax'),
            func.sum(Order.amount).label('total_amount'),
            func.sum(VehicalOrder.commission_amount).label('commission')
        ).join(VehicalOrder, Order.id == VehicalOrder.order_id).group_by(func.date(Order.created_at)).filter(func.date(Order.created_at) == date).all()


        result = [
            {
                'order_date': order_date.strftime('%Y-%m-%d'),
                'pax':pax,
                'total_amount': total_amount,
                'commission': commission
            }
            for order_date,pax, total_amount, commission in order_summary
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while generating the report.'}), 500

@blue_print.route("/get_single_day_order_details", methods=["GET"])
def getSingleDayOrderDetails():
    date = request.args.get('date')
    if not date:
        return {
            'status': 400,
            'message': 'date required'
        }
    try:
        # order_details = Order.query.filter(Order.created_at.like('%{date}%')).all()func.date(Order.created_at)
        order_details = Order.query.filter(func.date(Order.created_at) == date).all()
        result = [{'id': order.id,'name': order.serial_no,'pax': order.pax,'amount': order.amount,'payment_method': order.payment_method,'created_at': order.created_at} for order in order_details]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while generating the report.'}), 500 

# route to get report based on a given dates
@blue_print.route("/get_report_between_dates", methods=["GET"])
def generateReportBasedOnDates():

    startDate = request.args.get('firstdate')
    endDate = request.args.get('lastdate')
    if not startDate:
        return {
            'status': 400,
            'message': 'start date required'
        }
    
    if not endDate:
        return {
            'status': 400,
            'message': 'end date required'
        }

    try:
        order_summary = db.session.query(
            func.date(Order.created_at).label('order_date'),
            func.sum(Order.pax).label('pax'),
            func.sum(Order.amount).label('total_amount'),
            func.sum(VehicalOrder.commission_amount).label('commission')
        ).join(VehicalOrder, Order.id == VehicalOrder.order_id).group_by(func.date(Order.created_at)).filter(func.date(Order.created_at) >= startDate,func.date(Order.created_at) <= endDate).all()

        result = [
            {
                'order_date': order_date.strftime('%Y-%m-%d'),
                'pax':pax,
                'total_amount': total_amount,
                'commission': commission
            }
            for order_date,pax, total_amount, commission in order_summary
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while generating the report.'}), 500


@blue_print.route("/get_order_details_dates", methods=["GET"])
def getOrderDetailsOnDate():
    startDate = request.args.get('firstdate')
    endDate = request.args.get('lastdate')
    if not startDate:
        return {
            'status': 400,
            'message': 'start date required'
        }
    
    if not endDate:
        return {
            'status': 400,
            'message': 'end date required'
        }
    
    try:
        order_datails = Order.query.filter(and_(
            Order.created_at >= startDate,
            Order.created_at <= endDate
        )).all()

        order_list = [{'id': order.id,'name': order.serial_no,'pax': order.pax,'amount': order.amount,'payment_method': order.payment_method,'created_at': order.created_at} for order in order_datails]
        return jsonify(order_list), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while generating the report.'}), 500 
