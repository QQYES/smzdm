import json
import pickle
from time import sleep
from typing import List

from pyquery import PyQuery
from requests import request
from tqdm import tqdm


class Product:
    def __init__(self):
        self.title: str = ''
        self.url: str = ''
        self.comment_count: int = -1
        self.mall: str = ''
        self.collection_count: int = -1
        self.price: int = -1


class Spider:

    def __init__(self):
        self.base_url: str = 'https://www.smzdm.com/fenlei/yidongyingpan/h1c1s0f0t0p'
        self.request_headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
        self.products: List[Product] = []

    def get_products(self):
        for page_index in tqdm(range(3, 5)):
            html = request('GET', self.base_url + str(page_index), headers=self.request_headers).text
            if html is not None and html != '':
                # 初始化PyQuery
                doc: PyQuery = PyQuery(html)
                contents: List[PyQuery] = doc(".z-feed-content > .z-highlight > a").items()
                for content in contents:
                    product = Product()
                    product.title = eval(content.attr('onclick')[15:-1])['pagetitle']
                    product.url = content.attr('href')
                    product.mall = eval(content.attr('onclick')[15:-1])['商城']
                    product.price = content.text()
                    self.products.append(product)
                foots: List[PyQuery] = doc(".z-feed-foot > .z-feed-foot-l > .z-group-data span").items()
                for (index, foot) in enumerate(foots):
                    if isinstance(foot, PyQuery):
                        self.products[index].comment_count = int(foot.text())
            sleep(2)


if __name__ == '__main__':
    spider = Spider()
    spider.get_products()
    for product_cls in spider.products:
        print(product_cls.__dict__)
    spider.products.sort(key=lambda x: x.comment_count, reverse=True)
    print("-----------------------------------------------------------------------------------------------------")
    for product_cls in spider.products:
        print(product_cls.__dict__)
    with open('by_class.list', 'wb') as f:
        pickle.dump(spider.products, f)
