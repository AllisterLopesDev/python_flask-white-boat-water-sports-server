# predefined class for time
from datetime import datetime

# custom class for db connection
from db import db

class Vehical(db.Model):
    __tablename__ = 'vehical'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_no = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    contact = db.Column(db.String(45), nullable=False)
    commission_amount = db.Column(db.Double, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)