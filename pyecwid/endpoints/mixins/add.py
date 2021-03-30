class EndpointAddItemMixin:
    def add(self, item):
        ''' Adds a single item.
            Returns item_id
            Requires item to be a dict with valid structure
        '''
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        if not self.validator.check_paramater_is_valid_dict(item):
            return

        result = self.api.post_request(self.endpoint, item)

        if result.status_code != 200:
            raise UserWarning("Item not created.", result.status_code, result.text)

        return result.json()['id']
