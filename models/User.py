from db import db

class User():
    __tablename__ = 'credential'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)

    # constructor
    def __init__(self, email, password):
        self.email = email
        self.password = password