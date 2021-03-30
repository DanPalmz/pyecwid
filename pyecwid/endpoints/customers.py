from pyecwid.endpoints import EcwidEndpoint
from pyecwid.endpoints.mixins import (EndpointAddItem, EndpointDeleteItem,
    EndpointGetAll, EndpointGetById, EndpointGetByKeyword, EndpointUpdateItem)

class Customers(EcwidEndpoint, EndpointAddItem, EndpointDeleteItem,
    EndpointGetAll, EndpointGetById, EndpointGetByKeyword, EndpointUpdateItem):
    def __init__(self, api, validator=False):
        super().__init__(api, validator)
        self.endpoint = 'customers'


    def get_by_email(self, email):
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        params = {'email': email}

        result = self.api.get_request(self.endpoint, params)
        return result

    def get_by_name(self, name):
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        params = {'name': name}

        result = self.api.get_request(self.endpoint, params)
        return result
