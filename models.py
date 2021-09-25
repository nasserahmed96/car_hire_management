import pymysql

from database import Model

class Customer(Model):
    def __init__(self, cursor, first_name=None, last_name=None, middle_name=None,
                 email=None, password=None, phone_number=None):

        super(Customer, self).__init__(table_name="customers", cursor=cursor)
        self.initialize_attributes(first_name, last_name, middle_name,
                 email, password, phone_number)

    def initialize_attributes(self, first_name, last_name, middle_name, email, password, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

    def get_customer(self, customer_id):
        query = f"""SELECT users.* FROM {self.table_name} INNER JOIN users ON users.id=customers.user WHERE {self.table_name}.id={customer_id}"""
        data = self.get_object(customer_id, query)
        if data:
            first_name, last_name, middle_name, email, password, phone_number = data
            self.initialize_attributes(first_name, last_name, middle_name, email, password, phone_number)
            return self
        else:
            return None


    def __str__(self):
        return "{first_name} {middle_name} {last_name}".format(
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name)