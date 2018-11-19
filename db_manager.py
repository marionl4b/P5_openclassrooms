import mysql.connector
from mysql.connector import errorcode
import settings
import config
import OFF_request

request = OFF_request.RequestParser()


class DataInit:
    def __init__(self):
        self.categories, self.products = request.load_data()
        self.cnx = self.database_connexion()
        self.cursor = self.cnx.cursor(buffered=True)

        self.use_database()

    def database_connexion(self):
        """test config and connect to mysql server"""
        try:
            cnx = mysql.connector.connect(**config.CONFIG)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            return cnx

    def use_database(self):
        """test if PurBeurre exists and use it"""
        try:
            self.cnx.database = config.DB_NAME
            print("Database ready")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                exit(1)
