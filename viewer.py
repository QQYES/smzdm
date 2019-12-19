import pickle
from typing import List

from model import Product


class Viewer:
    def __init__(self, file_name):
        self.file_name: str = file_name
        with open(self.file_name, 'rb') as f:
            self.products: List[Product] = pickle.load(f)

    def view_products(self):
        for product in self.products:
            print(product.__dict__)

    def filter_by_price(self, price):
        self.products = list(filter(lambda x: x.price < price, self.products))

    def filter_by_mall(self, mall):
        self.products = list(filter(lambda x: x.mall == mall, self.products))

    def filter_by_keywords(self, keywords):
        self.products = list(filter(lambda x: not x.title.__contains__(keywords), self.products))


v = Viewer('data/显示器_167')
# v.filter_by_price(4500)
# v.filter_by_mall('京东')
# v.filter_by_keywords('芝华仕')
# v.filter_by_keywords('真皮')
v.view_products()
