import pickle
import re
from time import sleep
from typing import List

from pyquery import PyQuery
from requests import request
from tqdm import tqdm

from model import BrandProduct, Product


class Spider:

    def __init__(self):
        self.base_url: str = 'https://pinpai.smzdm.com/765/youhui/p'
        self.request_headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
        self.products: List[Product] = []

    def get_products(self):
        for page_index in tqdm(range(1, 31)):
            html = request('GET', self.base_url + str(page_index), headers=self.request_headers).text
            if html is not None and html != '':
                # 初始化PyQuery
                doc: PyQuery = PyQuery(html)
                contents: List[PyQuery] = doc(".right-list-detail").items()
                # 用于后期遍历追加index下标防止每次都只写第一页数组
                for content in contents:
                    product = BrandProduct()
                    product.title = content('.right-list-title > a').items().__next__().text()
                    product.url = content('.right-list-title > a').items().__next__().attr('href')
                    try:
                        product.price = float(
                            re.findall(r"\d+\.?\d*", content('.right-list-title > a > span').items().__next__().text())[
                                0])
                    except IndexError:
                        print("价格获取错误，错误内容:{}".format(product.__dict__))
                    product.comment_count = int(
                        content('.icon-zhikupinglun + .comment-number').items().__next__().text())
                    product.collection_count = int(
                        content('.icon-collect + .comment-number').items().__next__().text())
                    self.products.append(product)

            sleep(2)


if __name__ == '__main__':
    spider = Spider()
    spider.get_products()
    spider.products.sort(key=lambda x: x.comment_count, reverse=True)
    for product_cls in spider.products:
        print(product_cls.__dict__)
    with open('yaseshi', 'wb') as f:
        pickle.dump(spider.products, f)
