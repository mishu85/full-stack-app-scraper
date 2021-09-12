class Product:
    def __init__(self, name, price, link, store):
        self.name = name
        self.link = link
        self.price = price
        self.store = store

    def __str__(self):
        return f"{self.name}\n{self.price}\n{self.link}\n{self.store}"

    def to_dict(self):
        dict={
            'name': self.name,
            'link': self.link,
            'price': self.price,
            'store': self.store
        }
        return dict
