class EndpointDeleteItemMixin:
    def delete(self, item_id):
        ''' Deletes a single item.
            Returns deleteCount int
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        item_id = self.validator.get_str_of_value_or_false(item_id)
        if not item_id:
            raise ValueError("item_id not a valid number", item_id)
        else:
            endpoint = self.join_endpoint(item_id)

        result = self.api.delete_request(endpoint)

        if result.status_code != 200:
            raise UserWarning("Product not deleted.", result.status_code, result.text)

        return result.json()['deleteCount']
