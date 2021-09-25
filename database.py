from abc import abstractmethod
import pymysql
from pymysql.err import OperationalError


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


class Model(object):
    """
    A model object to
    """
    def __init__(self, table_name, cursor):
        self.table_name = table_name
        self.cursor = cursor

    @abstractmethod
    def initialize_attributes(self):
        pass

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
        If the query returned more than one record that means there is an integrity error
        """
        if self.cursor.rowcount > 1:
            print("The query returned more than one result")
            return None
        elif self.cursor.rowcount == 0:
            print("404 didn't found any results")
        else:
            return self.cursor.fetchall()
        return None