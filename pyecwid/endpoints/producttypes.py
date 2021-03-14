from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import (EndpointAddItem, EndpointDeleteItem, 
    EndpointGetAll, EndpointGetById, EndpointUpdateItem)
    
class ProductTypes(EcwidEndpoint, EndpointAddItem, EndpointDeleteItem, 
    EndpointGetAll, EndpointGetById, EndpointUpdateItem):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'classes'