from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import (EndpointAddItemMixin, EndpointDeleteItemMixin,
    EndpointGetAllUnpagedOnlyMixin, EndpointGetByIdMixin, EndpointUpdateItemMixin)

class ProductTypes(EcwidEndpoint, EndpointAddItemMixin, EndpointDeleteItemMixin,
    EndpointGetAllUnpagedOnlyMixin, EndpointGetByIdMixin, EndpointUpdateItemMixin):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'classes'
