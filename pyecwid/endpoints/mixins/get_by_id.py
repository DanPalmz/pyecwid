class EndpointGetByIdMixin:
    def get_by_id(self, item_id):
        ''' Returns a single item details.
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        item_id = self.validator.get_str_of_value_or_false(item_id)

        if not item_id:
            raise ValueError("item_id not a valid number")

        endpoint = self.join_endpoint(item_id)

        result = self.api.get_request(endpoint, collate_items=False)
        return result
