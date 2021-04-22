class EndpointGetByParamsMixin:
    def get_by_params(self, params, collate_items=True):
        ''' Searches endpoint with paramaters.
            Search endpoint by paramaters specified in dict.
            Eg:  { 'keyword': 'dragons', 'updatedFrom': '2011-05-01' }
            Returns List of all [items] found unless collate_items=False.
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        if not self.validator.check_paramater_is_valid_dict(params):
            return False

        result = self.api.get_request(self.endpoint, params, collate_items)
        return result
