from abc import abstractmethod
import pymysql
from pymysql.err import OperationalError, IntegrityError, ProgrammingError


class DatabaseConnection(object):
    """
    A singletone class to be used in the whole project
    """
    def __init__(self, database_name, user, password, host):
        self.connection = None
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.connect_to_db()
        self.items = None

    def connect_to_db(self):
        """
        Connect to the base and return a cursor object in case of success or None of case of errors
        :param database_name:
        :param user:
        :param password:
        :param host:
        :return:
        """
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database_name)
        except OperationalError as e:
            print(e)


    def get_cursor(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def get_connection(self):
        return self.connection


class Model(object):
    """
    A model object to
    """
    def __init__(self, table_name, cursor, connection):
        self.table_name = table_name
        self.cursor = cursor
        self.connection = connection

    @abstractmethod
    def initialize_attributes(self):
        pass

    def insert_new_object(self, table_name=None):
        if not table_name:
            table_name = self.table_name
        print("Table name: ", self.table_name)
        try:
            """
            Inserting a new object for that model, this function must be called after initialize_attributes,
            or initialize the attributes already in the constructor
            """
            query = f"""INSERT INTO {table_name}("""
            values = ""
            for item in self.items.keys():
                print("Item: ", self.items[item])
                if self.items[item]:
                    query += item + ","
                    values += "'" + str(self.items[item]) + "'" + ","
            query = query[:-1] + ") VALUES (" + values[:-1] + ")"
            print("Query: ", query)
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid
        except IntegrityError as e:
            print(e)
            self.connection.rollback()

    def update_object(self, object_id:int, new_items:dict, table_name=None):
        if not table_name:
            table_name = self.table_name
        try:
            """
            Updating an object for that model, this function must be called after initialize_attributes,
            or initialize the attributes already in the constructor
            """
            query = f"""UPDATE {table_name} SET """
            for item in new_items.keys():
                if new_items[item]:
                    query += f"""{item}='{new_items[item]}',"""
            query = query[:-1] + f" WHERE id={object_id}"
            print("Query: ", query)
            self.cursor.execute(query)
            #self.connection.commit()
            return self.cursor.lastrowid
        except IntegrityError as e:
            print(e)
            self.connection.rollback()

    def delete_object(self, object_id:int, table_name=None):
        """
        Delete an object from the current table or from the table specified by the user
        :param object_id:
        :return:
        """
        if not table_name:
            table_name = self.table_name

        if not self.get_object(object_id):
            print("Can't find the requested object")
            return None

        query = f"""DELETE FROM {table_name} WHERE id={object_id}"""
        print("Query", query)
        self.cursor.execute(query)
        self.connection.commit()
        print("Deleted")
        return 0

    def get_object(self, object_id:int, query=None):
        """
        :param object_id:
        :return: An object of the class Customer or None if no results found or in case of errors
        """
        if not query:
            query = f"""
            SELECT * FROM {self.table_name} WHERE {self.table_name}.id={object_id}
            """
        self.cursor.execute(query)
        """
        Return None in case of the rowcount is more than 1(IntegrityError) or rowcount is 0(No results)
        """
        if self.cursor.rowcount > 1 or self.cursor.rowcount == 0:
            print("Row count: ", self.cursor.rowcount)
            return None
        else:
            return self.cursor.fetchall()[0]
        return None