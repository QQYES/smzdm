from typing import List

from pyquery import PyQuery
from requests import request


class Product:
    def __init__(self):
        self.title: str = ''
        self.url: str = ''
        self.comment_numbe: int = ''
        self.mall: str = ''


class Spider:

    def __init__(self):
        self.base_url: str = 'https://www.smzdm.com/fenlei/yidongyingpan/p'
        self.request_params: dict = {"http.protocol.cookie-policy": "compatibility",
                                     "http.protocol.content-charset": "utf-8"}
        self.request_headers: dict = {
            "Cookie": "checkeduser=true; user_text=zhangss108_1; pass_text=01234567890;unicom=AyJlq0yCecw%3D; bigtypeid=0; expert=1; enterCount=563552; isAdoptBox=1; work_frist=1"}
        self.products: List[Product] = []

    def get_products(self):
        for page_index in range(30):
            html = request('GET', self.base_url + str(page_index), params=self.request_params,
                           headers=self.request_headers).text
            if html is not None and html != '':
                # 初始化PyQuery

                doc = PyQuery(html)
                for item in doc(".feed-block-title a").items():
                    product = Product()
                    product.title=item.text()
                    product.url = item.attr('href')
                    product.mall = item.
