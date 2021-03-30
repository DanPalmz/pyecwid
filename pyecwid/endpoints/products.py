from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import (EndpointAddItem, EndpointDeleteItem,
    EndpointGetAll, EndpointGetById, EndpointGetByKeyword, EndpointGetByParams, EndpointUpdateItem)

class Products(EcwidEndpoint, EndpointAddItem, EndpointDeleteItem,
    EndpointGetAll, EndpointGetById, EndpointGetByKeyword, EndpointGetByParams, EndpointUpdateItem):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'products'
