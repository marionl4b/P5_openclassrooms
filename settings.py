import os.path

TABLES = dict()

TABLES['product'] = (
    "CREATE TABLE `product` ("
    "  `product_name` varchar(100) NOT NULL,"
    "  `description` text,"
    "  `brand` varchar(100),"
    "  `API_link` varchar(200) NOT NULL,"
    "  `nutriscore` char(1),"
    "  PRIMARY KEY (product_name)"
    ") ENGINE=InnoDB")

TABLES['store'] = (
    "CREATE TABLE `store` ("
    "  `store_name` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`store_name`)"
    ") ENGINE=InnoDB")

TABLES['historic'] = (
    "CREATE TABLE `historic` ("
    "  `hist_id` smallint UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `hist_date` datetime NOT NULL,"
    "  `hist_product` varchar(100) NOT NULL,"
    "  `hist_substitute` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`hist_id`),"
    "  KEY (`hist_product`),"
    "  KEY (`hist_substitute`),"
    "  CONSTRAINT `fk_hist_product` FOREIGN KEY (`hist_product`) "
    "     REFERENCES `product` (`product_name`),"
    "  CONSTRAINT `fk_hist_substitute` FOREIGN KEY (`hist_substitute`) "
    "     REFERENCES `product` (`product_name`)"
    ") ENGINE=InnoDB")

TABLES['category_product'] = (
    "CREATE TABLE `category_product` ("
    "  `cp_category` varchar(100) NOT NULL,"
    "  `cp_product` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`cp_category`, `cp_product`),"
    "  CONSTRAINT `fk_cp_category` FOREIGN KEY (`cp_category`) "
    "     REFERENCES `category` (`category_name`),"
    "  CONSTRAINT `fk_cp_product` FOREIGN KEY (`cp_product`) "
    "     REFERENCES `product` (`product_name`)"
    ") ENGINE=InnoDB")

TABLES['store_product'] = (
    'CREATE TABLE `store_product` ('
    '  `sp_store` varchar(100) NOT NULL,'
    '  `sp_product` varchar(100) NOT NULL,'
    '  PRIMARY KEY (`sp_store`, `sp_product`),'
    '  CONSTRAINT `fk_sp_store` FOREIGN KEY (`sp_store`) '
    '     REFERENCES `store` (`store_name`),'
    '  CONSTRAINT `fk_sp_product` FOREIGN KEY (`sp_product`) '
    '     REFERENCES `product` (`product_name`)'
    ') ENGINE=InnoDB')


DIR_PATH = os.path.dirname(os.path.abspath(__file__))

R_COLLECTION = {'category': 'https://fr.openfoodfacts.org/categories.json',
                'product': 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}'
                           '&search_simple=1&action=process&&sort_by=unique_scans_n&page=1&json=1'
                }
