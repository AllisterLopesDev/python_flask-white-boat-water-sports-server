from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_mysqldb import MySQL
from db import db

from resources.auth import blue_print as UserAuthBluePrint
from resources.user import blue_print as UserBluePrint

app = Flask(__name__)



# CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/advanture_boat_trip'
db.init_app(app)
ma = Marshmallow(app)



@app.route('/',methods=['GET'])
def home():
    return 'WELCOME TO WHITE WATER ADVENTURE'



# route blueprint from resources
app.register_blueprint(UserAuthBluePrint)
app.register_blueprint(UserBluePrint)



if __name__ == '__main__':
    app.run(debug = True)