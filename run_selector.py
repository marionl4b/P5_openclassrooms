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
        cat_selected = self.select_category()
        prod_selected = self.select_product(cat_selected)
        self.show_product(prod_selected)
        substitute = self.show_substitute(cat_selected)

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

    def select_product(self, cat_selected):
        """show products from selected category and return index and name of the chosen one"""
        temp_crawl = []
        sql_select_query = "SELECT cp_product FROM category_product WHERE cp_category = %(category)s"
        self.cursor.execute(sql_select_query, cat_selected)
        rows = self.cursor.fetchall()
        for row in enumerate(rows):
            index = row[0]
            product = row[1][0]
            print(index, product)
            temp_crawl.append({"index": index, "product": product})
        prod_index = check_user_answer("Veuillez séléctionner un produit (chiffre)", temp_crawl)
        prod_selected = index_constructor(prod_index, temp_crawl)
        return prod_selected

    def show_product(self, prod_selected):
        """show attributes product and store_product from product selected by Mysql SELECT OUTER JOIN command)"""
        sql_select_query = "SELECT * FROM product WHERE product_name = %(product)s"
        self.cursor.execute(sql_select_query, prod_selected)
        rows = self.cursor.fetchall()
        for row in rows:
            print("#################### produit sélectionné #####################")
            print("nom : {}".format(row[0]))
            print("description : {}".format(row[1]))
            print("marque : {}".format(row[2]))
            print("url : {}".format(row[3]))
            print("nutriscore : {}".format(row[4]))
            print("")

    def show_substitute(self, cat_selected):
        """show attributes product from category selected and nutriscore by Mysql SELECT OUTER JOIN command)"""
        sql_select_query = "SELECT category_product.cp_product, product.* FROM category_product " \
                           "LEFT JOIN product ON category_product.cp_product = product.product_name " \
                           "WHERE category_product.cp_category = %(category)s ORDER BY product.nutriscore"
        self.cursor.execute(sql_select_query, cat_selected)
        rows = self.cursor.fetchall()
        i = -1
        for row in rows:
            i += 1
            if i < 1:
                substitute = row[0]
                print("#################### substitut #####################")
                print("nom : {}".format(row[1]))
                print("description : {}".format(row[2]))
                print("marque : {}".format(row[3]))
                print("url : {}".format(row[4]))
                print("nutriscore : {}".format(row[5]))
                print("")
                return substitute
