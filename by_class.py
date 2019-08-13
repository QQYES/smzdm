import json
import pickle
import re
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
        self.price: float = -1


class Spider:

    def __init__(self):
        self.base_url: str = 'https://www.smzdm.com/fenlei/bijibendiannao/h1c1s0f0t0p'
        self.request_headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
        self.products: List[Product] = []

    def get_products(self):
        for page_index in tqdm(range(1, 31)):
            html = request('GET', self.base_url + str(page_index), headers=self.request_headers).text
            if html is not None and html != '':
                # 初始化PyQuery
                doc: PyQuery = PyQuery(html)
                contents: List[PyQuery] = doc(".z-feed-content > .z-highlight > a").items()
                # 用于后期遍历追加index下标防止每次都只写第一页数组
                accumulate_index = self.products.__len__()
                for content in contents:
                    product = Product()
                    product.title = eval(content.attr('onclick')[15:-1])['pagetitle']
                    product.url = content.attr('href')
                    product.mall = eval(content.attr('onclick')[15:-1])['商城']
                    try:
                        product.price = float(re.findall(r"\d+\.?\d*", content.text())[0])
                    except IndexError:
                        print("价格获取错误，错误内容:{}".format(product.__dict__))
                    self.products.append(product)
                foots: List[PyQuery] = doc(".z-group-data > span").items()
                # foots里边是收藏数和评论数交替出现，因此交替加入数组
                for (index, foot) in enumerate(foots):
                    if isinstance(foot, PyQuery):
                        if index % 2 == 0:
                            # index的运算多加一个括号是为了强调先加然后在除的顺序
                            self.products[int(accumulate_index + (index / 2))].comment_count = int(foot.text())
                        else:
                            self.products[int(accumulate_index + (index / 2))].collection_count = int(foot.text())
            sleep(2)


if __name__ == '__main__':
    spider = Spider()
    spider.get_products()
    spider.products.sort(key=lambda x: x.comment_count, reverse=True)
    for product_cls in spider.products:
        print(product_cls.__dict__)
    with open('bijibendiannao.list', 'wb') as f:
        pickle.dump(spider.products, f)
