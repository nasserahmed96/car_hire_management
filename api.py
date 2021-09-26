from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import Customer
from database import DatabaseConnection
import status
from pytz import utc

class CustomerManager(object):
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

    def get_customer(self, customer_id):
        customer = Customer()
        customer = customer.get_customer(customer_id)
