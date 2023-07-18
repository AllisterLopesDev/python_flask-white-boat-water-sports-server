# Custom class imports
from db import db

class Credential(db.Model):
    __tablename__ = 'credential'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(120), nullable=False)