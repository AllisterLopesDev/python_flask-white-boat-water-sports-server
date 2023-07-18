# custom class for db connection
from db import db

# model class
from models.user import User


class Boat(db.Model):
    __tablename__ = 'boat'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    registration_no = db.Column(db.String(45), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id) ,nullable=False)


    # Backreferences to associate with user objects
    user = db.relationship('User', backref='boat', uselist=False)


