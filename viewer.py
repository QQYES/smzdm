import pickle
from typing import List

from model import Product

with open('yidongyingpan.list', 'rb') as f:
    products: List[Product] = pickle.load(f)

for product in products:
    print(product.__dict__)
