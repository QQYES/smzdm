import pickle
import re
from time import sleep
from typing import List

from pyquery import PyQuery
from requests import request
from tqdm import tqdm

from model import Product, ClassProduct


class Spider:

    def __init__(self):
        self.base_url: str = 'https://www.smzdm.com/fenlei/gutaiyingpan/h1c1s0f0t0p'
        self.request_headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
        self.products: List[Product] = []

    def get_products(self):
        for page_index in tqdm(range(1, 30)):
            html = request('GET', self.base_url + str(page_index), headers=self.request_headers).text
            if html is not None and html != '':
                # 初始化PyQuery
                doc: PyQuery = PyQuery(html)
                contents: List[PyQuery] = doc(".feed-row-wide").items()
                # 用于后期遍历追加index下标防止每次都只写第一页数组
                for content in contents:
                    product = ClassProduct()
                    try:
                        up = content('div.z-highlight > a').items().__next__()
                        product.title = eval(up.attr('onclick')[15:-1])['pagetitle']
                        product.url = up.attr('href')
                        product.mall = eval(up.attr('onclick')[15:-1])['商城']
                        product.price = float(re.findall(r"\d+\.?\d*", up.text())[0])
                        product.comment_count = int(
                            content('.icon-comment-o-thin + span').items().__next__().text())
                        product.collection_count = int(
                            content('.icon-star-o-thin + span').items().__next__().text())
                        self.products.append(product)
                    except Exception as e:
                        print("异常错误信息：{}".format(e))
                        print("价格获取错误，错误内容:{}".format(product.__dict__))
            sleep(2)


if __name__ == '__main__':
    spider = Spider()
    spider.get_products()
    spider.products.sort(key=lambda x: x.comment_count, reverse=True)
    for product_cls in spider.products:
        print(product_cls.__dict__)
    with open('data/gutaiyingpan', 'wb') as f:
        pickle.dump(spider.products, f)
