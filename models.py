import pymysql

from database import Model, ProgrammingError


class User(Model):
    def __init__(self, cursor, connection, table_name="users", first_name=None, last_name=None, middle_name=None,
                 email=None, phone_number=None):

        super(User, self).__init__(table_name=table_name, cursor=cursor, connection=connection)
        self.initialize_attributes(first_name, last_name, middle_name,
                                   email, phone_number)

    def initialize_attributes(self, first_name, last_name, middle_name, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.email = email
        self.phone_number = phone_number
        self.items = {"first_name": self.first_name,
                     "middle_name": self.middle_name,
                     "last_name": self.last_name,
                     "email": self.email,
                     "phone_number": self.phone_number
                     }
        return self

    def get_user(self, user_id, query=None):
        data = self.get_object(user_id, query)
        print("Data: ", data)
        if data:
            id, first_name, middle_name, last_name, phone_number, address, status, email = data
            self.initialize_attributes(first_name, last_name, middle_name, email, phone_number)
            return self
        else:
            return None

    def __str__(self):
        return "{first_name} {middle_name} {last_name}".format(
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name)


class Customer(User):
    def __init__(self, cursor, connection, first_name=None, last_name=None, middle_name=None,
                 email=None, phone_number=None):

        super(Customer, self).__init__( cursor, connection, table_name="customers", first_name=None, last_name=None, middle_name=None,
                 email=None, phone_number=None)

        self.user = self.initialize_attributes(first_name, last_name, middle_name,
                                   email, phone_number)


    def get_customer(self, customer_id):
        query = f"""SELECT users.* FROM {self.table_name} INNER JOIN users ON users.id=customers.user WHERE {self.table_name}.id={customer_id}"""
        data = self.get_object(customer_id, query)
        print("Data: ", data)
        if data:
            id, first_name, middle_name, last_name, phone_number, address, status, email = data
            self.initialize_attributes(first_name, last_name, middle_name, email, phone_number)
            return self.items
        else:
            return None

    def insert_new_customer(self):
        try:
            user_id = self.user.insert_new_object("users")
            if not user_id:
                print("An error has occured while creating the user")
            print("User id: ", user_id)
            self.items = {"user": user_id}
            customer_id = self.insert_new_object()
            print("Customer ID: ", customer_id)
        except ProgrammingError as e:
            print(e)

