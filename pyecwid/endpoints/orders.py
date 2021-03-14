from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import EndpointGetAll, EndpointGetById

class Orders(EcwidEndpoint, EndpointGetAll, EndpointGetById):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'orders'