import pickle
from typing import List

from model import Product


class Viewer:
    def __init__(self, file_name):
        self.file_name: str = file_name

    def view_products(self):
        with open(self.file_name, 'rb') as f:
            products: List[Product] = pickle.load(f)

        for product in products:
            print(product.__dict__)


Viewer('yaseshi.list').view_products()
