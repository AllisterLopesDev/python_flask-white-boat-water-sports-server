from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_mysqldb import MySQL
from db import db

from resources.auth import blue_print as UserAuthBluePrint
from resources.user import blue_print as UserBluePrint
from resources.boat import blue_print as BoatBluePrint
from resources.bookings import blue_print as BookingBluePrint
from resources.report import blue_print as ReportBluePrint
from resources.commission import blue_print as CommissionBluePrint
from resources.vehical_data import blue_print as VehicalBluePrint
from resources.delete import blue_print as DeleteOrderBluePrint

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
app.register_blueprint(BoatBluePrint)
app.register_blueprint(BookingBluePrint)
app.register_blueprint(ReportBluePrint)
app.register_blueprint(CommissionBluePrint)
app.register_blueprint(VehicalBluePrint)
app.register_blueprint(DeleteOrderBluePrint)


if __name__ == '__main__':
    app.run(debug = True)