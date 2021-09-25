from database import DatabaseConnection
from models import Customer

def start():
    database = DatabaseConnection(host='localhost', user='car_hire', password='C@r_H1r3', database_name='car_hire')
    cursor = database.get_cursor()
    customer = Customer("customers", cursor)
    customer.get_object(0)
    print(customer)


if __name__ == "__main__":
    start()