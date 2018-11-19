import OFF_request
import db_manager

request = OFF_request.RequestParser()
db_manager = db_manager.DataInit()


def check_user_answer(prompt, temp_crawl):
    """check if user answer is integer beteween 0 and max index of temp_crawl"""
    while 1:
        result = input(prompt)
        try:
            result = int(result)
            assert len(temp_crawl) > result >= 0
        except ValueError:
            print("Veuillez Entrer un chiffre ")
        except AssertionError:
            print("Veuillez Entrer un chiffre entre 0 et {} compris".format(len(temp_crawl) - 1))
        else:
            return result


def index_constructor(index, temp_crawl):
    """define object from index of user selection"""
    selection = ""
    for item in enumerate(temp_crawl):
        temp_crawl_index = item[0]
        if index == temp_crawl_index:
            selection = item[1]
    return selection


class SelectSubstitute:
    def __init__(self):
        self.categories, self.products = request.load_data()
        self.cnx = db_manager.cnx
        self.cursor = db_manager.cursor
        self.cnx.database = db_manager.cnx.database

        self.selection()

    def selection(self):
        """run methodes from class for substitute selection"""
        self.select_category()

    def select_category(self):
        """show catgories and return index and name of the chosen one"""
        temp_crawl = []
        for item in enumerate(self.categories):
            index = item[0]
            category = item[1].get("name")
            print(index, category)
            temp_crawl.append({"index": index, "category": category})
        cat_index = check_user_answer("Veuillez séléctionner une catégorie (chiffre)", temp_crawl)
        cat_selected = index_constructor(cat_index, temp_crawl)
        return cat_selected