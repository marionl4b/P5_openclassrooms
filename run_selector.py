# !/usr/bin/env python3
# coding: utf-8

import OFF_request
import db_manager
import datetime

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
            if len(temp_crawl) == 1:
                result = 1
                return result
            else:
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
    """run user selection by categories and products, show products and substitutes details
     and manage historic for user searches"""
    def __init__(self):
        self.categories, self.products = request.load_data()
        self.cnx = db_manager.cnx
        self.cursor = db_manager.cursor
        self.cnx.database = db_manager.cnx.database

    def selection(self):
        """run methodes from class for substitute selection"""
        cat_selected = self.select_category()
        prod_selected = self.select_product(cat_selected)
        self.show_product(prod_selected)
        substitute = self.show_substitute(cat_selected)
        self.add_to_historic(prod_selected, substitute)

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
        stores = self.select_store(prod_selected)
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
            print("points de vente : {}".format(stores))
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
                sub_store = {"product": row[0]}
                stores = self.select_store(sub_store)
                print("#################### substitut #####################")
                print("nom : {}".format(row[1]))
                print("description : {}".format(row[2]))
                print("marque : {}".format(row[3]))
                print("url : {}".format(row[4]))
                print("nutriscore : {}".format(row[5]))
                print("points de vente : {}".format(stores))
                print("")
                return substitute

    def select_store(self, prod_selected):
        """select stores for each products in store_product table"""
        sql_select_query = "SELECT sp_store FROM store_product WHERE sp_product = %(product)s"
        self.cursor.execute(sql_select_query, prod_selected)
        rows = self.cursor.fetchall()
        stores = []
        for row in rows:
            if row[0] != "":
                stores.append(row[0])
            else:
                stores.append("nc")
        stores = ", ".join(stores)
        return stores

    def add_to_historic(self, prod_selected, substitute):
        """ask user to save his last search"""
        while 1:
            user_answer = input("Ajouter à l'historique ? (O/N)")
            if user_answer == "O":
                self.insert_historic(prod_selected, substitute)
                break
            elif user_answer == "N":
                break
            else:
                print("Veuillez entree (O/N)")

    def insert_historic(self, prod_selected, substitute):
        """prepare and insert data attributes for historic"""
        now = datetime.datetime.now()
        hist_data = (now.strftime("%Y-%m-%d %H:%M:%S"), prod_selected.get("product"), substitute)
        sql_update_query = "INSERT IGNORE INTO historic (hist_date, hist_product, hist_substitute) " \
                           "VALUES (%s, %s, %s)"
        self.cursor.execute(sql_update_query, hist_data)
        self.cnx.commit()
        print("Dernière recherche ajoutée à l'historique")

    def show_historic(self):
        """show historic of substitute selections"""
        print("#################### historique #####################")
        temp_crawl = []
        sql_select_query = "SELECT * FROM historic"
        self.cursor.execute(sql_select_query)
        rows = self.cursor.fetchall()
        for row in rows:
            print("------------------------------")
            print("recherche n°{}".format(row[0]))
            print("date : {}".format(row[1]))
            print("produit : {}".format(row[2]))
            print("substitut : {}".format(row[3]))
            print("")
            temp_crawl.append({"index": row[0], "product": row[2], "substitute": row[3]})
        self.show_historic_details(temp_crawl)

    def show_historic_details(self, temp_crawl):
        """select the id of a search to show its detailed products and substitutes"""
        product = dict()
        substitute = dict()
        hist_select = check_user_answer("Veuillez séléctionner la recherche dont "
                                        "vous voulez afficher les détails (chiffre)", temp_crawl)
        hist_number = {"index": hist_select}
        sql_select_query = "SELECT hist_product, hist_substitute FROM historic " \
                           "WHERE historic.hist_id = %(index)s"
        self.cursor.execute(sql_select_query, hist_number)
        rows = self.cursor.fetchall()
        for row in rows:
            product = {"product": row[0]}
            substitute = {"product": row[1]}
        self.show_product(product)
        self.show_product(substitute)
