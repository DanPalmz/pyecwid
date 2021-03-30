class EndpointUpdateItemMixin:
    def update(self, item_id, values):
        ''' Update a single item.
            Requires values to update in dict
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        item_id = self.validator.get_str_of_value_or_false(item_id)
        if not item_id:
            raise ValueError("item_id not a valid number", item_id)
        else:
            endpoint = self.join_endpoint(item_id)

        if not self.validator.check_paramater_is_valid_dict(values):
            return False

        result = self.api.put_request(endpoint, values)
        return result
