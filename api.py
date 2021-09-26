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

    @marshal_with(customer_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('middle_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        parser.add_argument('phone_number', type=str, required=True)
        args = parser.parse_args()
        customer = Customer(cursor=self.cursor, connection=self.connection,
                            first_name=args['first_name'],
                            middle_name=args['middle_name'],
                            last_name=args['last_name'],
                            email=args['email'],
                            phone_number=args['phone_number'])
        result = customer.insert_new_customer()
        if not result:
            abort(status.HTTP_400_BAD_REQUEST, message="An error has occured while saving")
        return (customer, status.HTTP_201_CREATED)

    @marshal_with(customer_fields)
    def get(self, id):
        customer = Customer(cursor=self.cursor, connection=self.connection)
        customer = customer.get_customer(id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, message="Can't find the requested Customer")
        else:
            return customer

    def delete(self, id):
        customer = Customer(cursor=self.cursor, connection=self.connection)
        result = customer.delete_customer(id)
        if not result:
            abort(status.HTTP_404_NOT_FOUND, message="Can't find the requested Customer")
        return ("Deleted", status.HTTP_200_OK)

customer_manager = CustomerManager()

def run_flask_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(CustomerManager, '/api/get_customer/<int:id>',
                     '/api/create_customer',
                     '/api/delete_customer/<int:id>')
    app.run()

if __name__ == "__main__":
    run_flask_app()


