# !/usr/bin/env python3
# coding: utf-8

import mysql.connector
from mysql.connector import errorcode
from src import OFF_request, config, settings

request = OFF_request.RequestParser()


def database_connexion():
    """test config and connect to mysql server"""
    try:
        cnx = mysql.connector.connect(**config.CONFIG)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            exit(1)
        else:
            print(err)
            exit(1)
    else:
        return cnx


class DataInit:
    """Init database connexion, tables and inserted data"""
    def __init__(self):
        self.categories, self.products = request.load_data()
        self.cnx = database_connexion()
        self.cursor = self.cnx.cursor(buffered=True)

        self.use_database()
        self.create_tables()
        self.insert_data()

    def use_database(self):
        """test if PurBeurre exists and use it"""
        try:
            self.cursor.execute("USE {}".format(config.DB_NAME))
            print("Database ready")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                self.create_database()
            else:
                print(err)
                exit(1)
        else:
            self.cnx.database = config.DB_NAME

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
                print("Creating table : {}".format(table_name), end='\n')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("=> already exists.")
                else:
                    print(err.msg)
                    exit(1)

    def insert_data(self):
        """select table defined in settings and specify insertion query"""
        for table in settings.TABLES:
            if table == "category":
                query = "INSERT IGNORE INTO category (category_name) VALUES (%(name)s)"
                self.data_dict_constructor("category", query, self.categories)
            elif table == "product":
                query = "INSERT IGNORE INTO product (product_name, description, brand, API_link, nutriscore)" \
                        "VALUES (%(name)s, %(desc)s, %(brand)s, %(url)s, %(nutriscore)s)"
                self.data_dict_constructor("product", query, self.products)
            elif table == "store":
                query = "INSERT IGNORE INTO store (store_name) VALUES (%(name)s)"
                self.data_dict_constructor("store", query, self.products)
            elif table == "category_product":
                query = "INSERT IGNORE INTO category_product (cp_category, cp_product) " \
                        "VALUES (%(category)s, %(product)s)"
                self.data_dict_constructor("category_product", query, self.products)
            elif table == "store_product":
                query = "INSERT IGNORE INTO store_product (sp_store, sp_product) " \
                        "VALUES (%(store)s, %(product)s)"
                self.data_dict_constructor("store_product", query, self.products)
            else:
                pass
        print("data inserted")

    def data_dict_constructor(self, table, query, crawling_list):
        """select data for each table and store it in clean dictionaries"""
        for item in crawling_list:
            if table == "category" or table == "product":
                data_dict = item
                self.check_data(table, query, data_dict)
            elif table == "store":
                stores = item["store"].split(",")
                for store in stores:
                    data_dict = {"name": store}
                    self.check_data(table, query, data_dict)
            elif table == "category_product":
                prod_categories = item["categories"].split(",")
                for cat in prod_categories:
                    data_dict = {"category": cat, "product": item["name"]}
                    self.check_data(table, query, data_dict)
            elif table == "store_product":
                prod_stores = item["store"].split(",")
                for store in prod_stores:
                    data_dict = {"store": store, "product": item["name"]}
                    self.check_data(table, query, data_dict)
            else:
                pass

    def check_data(self, table, query, data_dict):
        """insert data from temp dictionary into table if don't already exists"""
        try:
            self.cursor.execute("SELECT EXISTS(SELECT * FROM {})".format(table))
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            self.cnx.rollback()
        else:
            self.cursor.execute(query, data_dict)
            self.cnx.commit()
