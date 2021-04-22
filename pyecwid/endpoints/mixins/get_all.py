class EndpointGetAllMixin:
    def get(self, collate_items=True):
        ''' Get all items for endpoint.
            Returns List of all [items] unless collate_items=False.
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        result = self.api.get_request(self.endpoint, collate_items=collate_items)
        return result

class EndpointGetAllUnpagedOnlyMixin:
    def get(self, collate_items=False):
        ''' Send get request for for endpoint.
            Does not handle pagination.  Returns all data elements.
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        result = self.api.get_request(self.endpoint, collate_items=False)
        return result
