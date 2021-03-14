from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import (EndpointAddItem, EndpointDeleteItem, 
    EndpointGetAll, EndpointGetById, EndpointGetByParams, EndpointUpdateItem)
    
class Coupons(EcwidEndpoint, EndpointAddItem, EndpointDeleteItem, 
    EndpointGetAll, EndpointGetById, EndpointGetByParams, EndpointUpdateItem):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'discount_coupons'