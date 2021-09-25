import pymysql

from database import Model

class Customer(Model):
    def __init__(self, table_name, cursor, first_name=None, last_name=None, middle_name=None,
                 email=None, password=None, phone_number=None):

        super(Customer, self).__init__(table_name, cursor)
        self.initialize_attributes(first_name, last_name, middle_name,
                 email, password, phone_number)

    def initialize_attributes(self, first_name, last_name, middle_name,
                 email, password, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

    def get_object(self, object_id:int, query=None):
        """
        :param object_id:
        :return: An object of the class Customer or None if no results found or in case of errors
        """
        if not query:
            query = """
            SELECT users.* FROM {table_name} INNER JOIN users ON users.id=customers.user WHERE customers.id={object_id}
            """.format(table_name=self.table_name, object_id=object_id)
        self.cursor.execute(query)
        if self.cursor.rowcount > 1:
            print("The query returned more than one result")
            return None
        elif self.cursor.rowcount == 0:
            print("404 didn't found any results")
        else:
            data = self.cursor.fetchall()
            first_name, middle_name, last_name, email, phone_number, password = data[0]
            self.initialize_attributes(first_name=first_name,
                                       middle_name=middle_name,
                                       last_name=last_name,
                                       email=email,
                                       phone_number=phone_number,
                                       password=password)
            """
            The user will only this to assign it to another object, anyway the user can use the current object
            """
            return self
        return None

    def __str__(self):
        return "{first_name} {middle_name} {last_name}".format(
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name)