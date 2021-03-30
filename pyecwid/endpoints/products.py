from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import (EndpointAddItemMixin, EndpointDeleteItemMixin,
    EndpointGetAllMixin, EndpointGetByIdMixin, EndpointGetByKeywordMixin, EndpointGetByParamsMixin, EndpointUpdateItemMixin)

class Products(EcwidEndpoint, EndpointAddItemMixin, EndpointDeleteItemMixin,
    EndpointGetAllMixin, EndpointGetByIdMixin, EndpointGetByKeywordMixin, EndpointGetByParamsMixin, EndpointUpdateItemMixin):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'products'
