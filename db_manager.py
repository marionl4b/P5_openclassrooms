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
        self.create_tables()

    def database_connexion(self):
        """test config and connect to mysql server"""
        try:
            cnx = mysql.connector.connect(**config.CONFIG)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                self.create_database()
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
                self.create_database()
            else:
                print(err)
                exit(1)

    def create_database(self):
        """create PurBeurre database"""
        try:
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(config.DB_NAME))
            print("Database {} created successfully.".format(config.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        else:
            self.cnx.database = config.DB_NAME

    def create_tables(self):
        """create tables defined in settings"""
        for table_name in settings.TABLES:
            table_description = settings.TABLES[table_name]
            try:
                print("Creating table : {} ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("=> already exists.")
                else:
                    print(err.msg)
                    exit(1)
