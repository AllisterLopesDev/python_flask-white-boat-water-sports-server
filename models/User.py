# Predefined class imports
from datetime import datetime

# Custom class imports
from db import db

# Model classes **required**
from models.credential import Credential

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    role = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    contact = db.Column(db.String(45), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    credential_id = db.Column(db.Integer, db.ForeignKey(Credential.id) ,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    # Backreferences to associate with credential objects
    credential = db.relationship('Credential', backref='user', uselist=False)