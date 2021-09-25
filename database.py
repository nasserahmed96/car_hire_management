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
