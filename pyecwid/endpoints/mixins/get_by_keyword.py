class EndpointGetByKeywordMixin:
    def get_by_keyword(self, keyword, collate_items=True):
        ''' Searches endpoint for specific keyword.
            Returns List of all [items] unless collate_items=False.
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        params = {'keyword': keyword}

        result = self.api.get_request(self.endpoint, params, collate_items)
        return result
