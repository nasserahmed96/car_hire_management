from database import DatabaseConnection
from models import Customer


def start():
    database = DatabaseConnection(host='localhost', user='car_hire', password='C@r_H1r3', database_name='car_hire')
    connection = database.get_connection()
    cursor = database.get_cursor()
    delete_customer(cursor, connection)
    #insert_new_customer(cursor, connection)

def delete_customer(cursor, connection):
    customer = Customer(cursor=cursor, connection=connection)
    customer.delete_object(1)

def insert_new_customer(cursor, connection):

    customer = Customer(cursor=cursor, connection=connection, first_name="Nasser",
                        middle_name="Ahmed",
                        last_name="Ismaiel",
                        email="abdelnasserahmed@gmail.com",
                        phone_number="01091238275")

    customer.get_customer(1)
    print("Customer: ", customer)


if __name__ == "__main__":
    start()