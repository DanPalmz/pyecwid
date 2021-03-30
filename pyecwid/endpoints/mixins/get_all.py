class EndpointGetAll:
    def get(self, collate_items=True):
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        result = self.api.get_request(self.endpoint, collate_items=collate_items)
        return result

class EndpointGetAllUnpagedOnly:
    def get(self, collate_items=False):
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        result = self.api.get_request(self.endpoint, collate_items=False)
        return result
