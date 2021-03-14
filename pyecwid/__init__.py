from pyecwid.ecwidapi import EcwidAPI
from pyecwid.ecwidapi_mock import EcwidAPIMock
from pyecwid.endpoints import Coupons, Customers, Orders, Products, ProductTypes

__all__ = ['Ecwid', 'EcwidAPI']


class Ecwid():
    def __init__(self, *args, **kwargs):
        self.api = EcwidAPI(*args, **kwargs)
        self.coupons = Coupons(self.api)
        self.customers = Customers(self.api)
        self.orders = Orders(self.api)
        self.products = Products(self.api)
        self.producttypes = ProductTypes(self.api)


class EcwidMock():
    def __init__(self, *args, **kwargs):
        self.api = EcwidAPIMock(*args, **kwargs)
        self.coupons = Coupons(self.api)
        self.customers = Customers(self.api)
        self.orders = Orders(self.api)
        self.products = Products(self.api)
        self.producttypes = ProductTypes(self.api)

