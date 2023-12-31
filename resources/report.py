from flask import Blueprint, jsonify, request
from sqlalchemy import func, and_, cast, Date
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
        return jsonify({
            'status': 400,
            'message': 'Date is required'
        }), 400

    try:
        # Your query for order summary based on the given date
        order_summary = db.session.query(

            func.date(Order.created_at).label('order_date'),
            func.sum(Order.pax).label('pax'),
            func.sum(Order.amount).label('total_amount'),
            func.sum(VehicalOrder.commission_amount).label('commission')
        ).join(VehicalOrder, Order.id == VehicalOrder.order_id).filter(func.date(Order.created_at) == date).all()

        # Query to get the sum of 'gpay' for the given date
        gpay_sum = db.session.query(func.sum(Order.amount)).filter(Order.payment_method == 'upi', Order.created_at == date).scalar()
        cash_sum = db.session.query(func.sum(Order.amount)).filter(Order.payment_method == 'cash', Order.created_at == date).scalar()
        result = [
            {
                'order_date': order_date.strftime('%Y-%m-%d'),
                'pax': pax,
                'total_amount': total_amount,
                'commission': commission,
                'gpay': 0 if not gpay_sum else gpay_sum,
                'cash': 0 if not cash_sum else cash_sum
            }
            for order_date, pax, total_amount, commission in order_summary
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
        result = [{'id': order.id,'serial-no': order.serial_no,'pax': order.pax,'amount': order.amount,'payment-method': order.payment_method,'created-at': order.created_at} for order in order_details]
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
        # order_datails = Order.query.filter(and_(
        #     Order.created_at >= startDate,
        #     Order.created_at <= endDate
        # )).all()

        # order_list = [{'id': order.id,'name': order.serial_no,'pax': order.pax,'amount': order.amount,'payment_method': order.payment_method,'created_at': order.created_at} for order in order_datails]
        # return jsonify(order_list), 200

        query = db.session.query(
            func.date(Order.created_at).label('order_date'),
            func.count(Order.id).label('no_of_orders'),
            func.sum(Order.amount).label('income'),
            func.sum(VehicalOrder.commission_amount).label('commission_amount')
        ).join(VehicalOrder, Order.id == VehicalOrder.order_id).filter(func.date(Order.created_at).between(startDate, endDate)).group_by(func.date(Order.created_at)).all()

        result = []
        for row in query:
            result.append({
                'order_date': row.order_date,
                'no_of_orders': row.no_of_orders,
                'income': row.income,
                'commission_amount': row.commission_amount,
                'profit': row.income-row.commission_amount
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while generating the report.'}), 500 
    


@blue_print.route("/day-report", methods=["GET"])
def generate_day_report():
    date = request.args.get('date')

    if not date:
        return jsonify({
            'message': 'Date parameter is required.',
            'status': 400,
            'data': False
        }), 400
    
    # query to filter results by date
    query = db.session.query(
        Order.amount,
        Order.pax,
        VehicalOrder.commission_amount,
        Order.payment_method,
        Order.created_at
    ).filter(
        #Order.created_at == date
        cast(Order.created_at, Date) == date
    ).outerjoin(
        VehicalOrder, Order.id == VehicalOrder.order_id
    )

    results = query.all()

    if not results:
        # No data for the specified date
        return jsonify({
            'message': 'No data found for the given date.',
            'status': 401,
        }), 401

    payment_mode = {
        'upi': 0,
        'cash': 0
    }

    # Initialize variables
    total_amount = 0
    total_commission_amount = 0
    total_profit_amount = 0
    total_pax = 0
    total_orders = 0

    for result in results:
        total_orders += 1
        amount = result.amount
        commission_amount = result.commission_amount
        payment_method = result.payment_method

        # total pax
        total_pax += result.pax
        # total amount
        total_amount += amount
        # total commission

        if commission_amount is not None:
            total_commission_amount += commission_amount
            # total profit
            total_profit_amount = total_profit_amount + (amount - commission_amount)
        else:
            # total profit if commission is none
            total_profit_amount += amount
        
        if payment_method == 'upi' or payment_method == 'UPI':
            payment_mode['upi'] += amount
        elif payment_method == 'cash' or payment_method == 'CASH':
            payment_mode['cash'] += amount

    response = {
        'amount': total_amount,
        'pax': total_pax,
        'commission': total_commission_amount,
        'profit': total_profit_amount,
        'payment-mode': payment_mode,
        'date': date,
        'orders': total_orders
    }

    return jsonify(response), 200