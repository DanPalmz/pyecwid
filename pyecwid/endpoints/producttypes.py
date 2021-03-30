from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import (EndpointAddItem, EndpointDeleteItem, 
    EndpointGetAllUnpagedOnly, EndpointGetById, EndpointUpdateItem)
    
class ProductTypes(EcwidEndpoint, EndpointAddItem, EndpointDeleteItem, 
    EndpointGetAllUnpagedOnly, EndpointGetById, EndpointUpdateItem):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'classes'
