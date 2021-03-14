class EndpointGetAll:
    def get(self):
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        result = self.api.get_request(self.endpoint)
        return result
