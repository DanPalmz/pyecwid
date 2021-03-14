from pyecwid.ecwidapi import EcwidAPI
from pyecwid.ecwidapi_mock import EcwidAPIMock
from pyecwid.endpoints import Products, Orders
class Ecwid():
    def __init__(self, *args, **kwargs):
        self.api = EcwidAPI(*args, **kwargs)
        self.products = Products(self.api)
        self.orders = Orders(self.api)


class EcwidMock():
    def __init__(self, *args, **kwargs):
        self.api = EcwidAPIMock(*args, **kwargs)
        self.products = Products(self.api)
        self.orders = Orders(self.api)

