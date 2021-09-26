from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import Customer
from database import DatabaseConnection
import status
from pytz import utc

customer_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'middle_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone_number': fields.String
}
class CustomerManager(Resource):

    def __init__(self):
        database = DatabaseConnection(host='localhost', user='car_hire', password='C@r_H1r3', database_name='car_hire')
        self.connection = database.get_connection()
        self.cursor = database.get_cursor()

    def insert_new_customer(self):
        customer = Customer(cursor=self.cursor, connection=self.connection,
                            first_name="Nasser",
                            middle_name="Ahmed",
                            last_name="Ismaiel",
                            email="abdelnasserahmed@gmail.com",
                            phone_number="01091238275")
        customer.insert_new_customer()

    @marshal_with(customer_fields)
    def get(self, id):
        customer = Customer(cursor=self.cursor, connection=self.connection)
        customer = customer.get_customer(id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, message="Can'r find the requested Customer")
        else:
            return customer

customer_manager = CustomerManager()

def run_flask_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(CustomerManager, '/api/get_customer/<int:id>')
    app.run()

if __name__ == "__main__":
    run_flask_app()


