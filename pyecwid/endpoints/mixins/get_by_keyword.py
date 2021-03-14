class EndpointByKeyword:
    def get_by_keyword(self, keyword):
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        params = {'keyword': keyword}

        result = self.api.get_request(self.endpoint, params)
        return result