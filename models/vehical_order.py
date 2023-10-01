from flask import Flask, request, jsonify
from db import db
from models.order import Order
from models.vehical import Vehical
from sqlalchemy.dialects.mysql import TINYINT


class VehicalOrder(db.Model):
    __tablename__ = 'vehical_order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehical_id = db.Column(db.Integer, db.ForeignKey(Vehical.id) ,nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.id) ,nullable=False)
    commission_amount = db.Column(db.Double, nullable=False)
    payment_status = db.Column(TINYINT(unsigned=True),default=False)



    # Backreferences to associate with vehical objects
    vehical = db.relationship('Vehical', backref='vehical_order', uselist=False)
    order = db.relationship('Order', backref='vehical_order', uselist=False)