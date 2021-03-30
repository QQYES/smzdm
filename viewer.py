import pickle
from typing import List

from model import Product


class Viewer:
    def __init__(self, file_name):
        self.file_name: str = file_name
        with open(self.file_name, 'rb') as f:
            self.products: List[Product] = pickle.load(f)

    def view_products(self):
        for index, product in enumerate(self.products):
            print(product.__dict__)
            # if index >= 200:
            #     break

    def filter_by_price_more(self, price):
        self.products = list(filter(lambda x: x.price > price, self.products))

    def filter_by_price_less(self, price):
        self.products = list(filter(lambda x: x.price < price, self.products))

    def filter_by_mall(self, mall):
        self.products = list(filter(lambda x: x.mall == mall, self.products))

    def filter_by_keywords(self, keywords):
        self.products = list(filter(lambda x: x.title.__contains__(keywords), self.products))

    def filter_by_not_keywords(self, keywords):
        self.products = list(filter(lambda x: not x.title.__contains__(keywords), self.products))


v = Viewer('data/热水器_141')
# v.filter_by_price_more(8000)
# v.filter_by_price_less(15000)
# v.filter_by_mall('京东')
# v.filter_by_keywords('C3')
# v.filter_by_keywords('林内')
v.filter_by_keywords('燃气')
# v.filter_by_not_keywords('NB')
# v.filter_by_not_keywords('洗烘')
# v.filter_by_not_keywords('单人')
# v.filter_by_not_keywords('电动')
# v.filter_by_not_keywords('芝华仕')
# v.filter_by_not_keywords('真皮')
v.view_products()
