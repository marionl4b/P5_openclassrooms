# !/usr/bin/env python3
# coding: utf-8

import os.path
import requests
import json
import settings


class RequestParser:

    def __init__(self):
        self.search_response = {}
        self.categories = []
        self.products = []
        self.data = {}

        self.load_data()

    def request_constructor(self, url, search_term, tag):
        """use url of R_COLLECTION in settings.py for requests for API OpenFoodFacts"""
        if search_term != "NULL":
            url = url.format(search_term)
        r = requests.get(url)
        response = r.json()
        self.search_response = response[tag]

    def crawl_data(self, data_type):
        """crawl search_response to prepare data to load for database insert"""
        i = 0
        cat = {}
        prod = {}
        for term in self.search_response:
            if data_type == 'category' and term['products'] > 6000:
                i += 1
                cat[i] = {"name": term['name']}
                self.categories.append(cat[i])
            elif data_type == 'product':
                nutrigrade = "".join(term["nutrition_grades_tags"])
                if nutrigrade in ("a", "b", "c", "d", "e"):
                    i += 1
                    prod[i] = {"name": term['product_name_fr'], "url": term['url'], "desc": term['generic_name_fr'],
                               "brand": term['brands'], "categories": term['categories'], "store": term['stores'],
                               "nutriscore": nutrigrade}
                    self.products.append(prod[i])
                else:
                    pass

    def save_data(self, filename):
        """json dump of data"""
        with open(settings.DIR_PATH + '/' + filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def load_data(self):
        """load data from OFF_data.json if dump already exists. If not run requests, crawling and saving data"""
        if not os.path.isfile("{}/OFF_data.json".format(settings.DIR_PATH)):
            self.request_constructor(settings.R_COLLECTION['category'], 'NULL', 'tags')
            self.crawl_data('category')
            i = 0
            for item in self.categories:
                i += 1
                cat = item.get("name")
                self.request_constructor(settings.R_COLLECTION['product'], cat, 'products')
                self.crawl_data('product')

            self.data = {"categories": self.categories, "products": self.products}
            self.save_data('OFF_data.json')
        else:
            with open("{}/OFF_data.json".format(settings.DIR_PATH), 'r') as f:
                self.data = json.load(f)
                self.categories = self.data["categories"]
                self.products = self.data["products"]
        return self.categories, self.products
