class Product:
    def __init__(self):
        self.title: str = ''
        self.url: str = ''
        self.comment_count: int = -1
        self.collection_count: int = -1
        self.price: float = -1


class BrandProduct(Product):
    def __init__(self):
        super().__init__()


class ClassProduct(Product):
    def __init__(self):
        super().__init__()
        self.mall: str = ''
