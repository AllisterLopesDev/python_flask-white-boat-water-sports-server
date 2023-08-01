# Predefined class imports
from datetime import datetime

# Custom class imports
from db import db

# model class
from models.vehical import Vehical

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_no = db.Column(db.String(45), nullable=False)
    pax = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Double, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)