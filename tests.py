from database import DatabaseConnection
from models import Customer


def start():
    database = DatabaseConnection(host='localhost', user='car_hire', password='C@r_H1r3', database_name='car_hire')
    cursor = database.get_cursor()
    insert_new_customer(cursor)

def insert_new_customer(cursor):
    customer = Customer(cursor=cursor,first_name="Nasser",
                        middle_name="Ahmed",
                        last_name="Ismaiel",
                        email="abdelnasserahmed@gmail.com",
                        password="secret",
                        phone_number="01091238274")
    customer.get_customer(0)
    print(customer)


if __name__ == "__main__":
    start()