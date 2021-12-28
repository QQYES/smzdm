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


v = Viewer('data/插排_30')
# v.filter_by_price_more(60)
# v.filter_by_price_less(100)
# v.filter_by_mall('京东')
# v.filter_by_keywords('云台')
# v.filter_by_keywords('米')
# v.filter_by_keywords('垫')
# v.filter_by_not_keywords('苹果')
# v.filter_by_not_keywords('迷你')
# v.filter_by_not_keywords('mini')
# v.filter_by_not_keywords('辽宁号')
# v.filter_by_not_keywords('芝华仕')
# v.filter_by_not_keywords('真皮')
v.view_products()
