from .endpoint_mixin import EndpointMixinBase

class EndpointGetByKeyword(EndpointMixinBase):
    def get_by_keyword(self, keyword, collate_items=True):
        if not self.endpoint:
            raise ValueError("endpoint not initialised")

        params = {'keyword': keyword}

        result = self.api.get_request(self.endpoint, params, collate_items)
        return result
