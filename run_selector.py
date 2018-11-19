import OFF_request
import db_manager

request = OFF_request.RequestParser()
db_manager = db_manager.DataInit()


class SelectSubstitute:
    def __init__(self):
        self.categories, self.products = request.load_data()
        self.cnx = db_manager.cnx
        self.cursor = db_manager.cursor
        self.cnx.database = db_manager.cnx.database

    def selection(self):
        """run methodes from class for substitute selection"""
        pass