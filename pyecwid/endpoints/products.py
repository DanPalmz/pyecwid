from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import EndpointGetAll, EndpointGetById, EndpointByKeyword, EndpointByParams

class Products(EcwidEndpoint, EndpointGetAll, EndpointGetById, EndpointByKeyword, EndpointByParams):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'products'