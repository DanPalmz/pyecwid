class EcwidEndpoint:
    endpoint = ''

    def __init__(self, api, validator):
        self.api = api
        if not validator:
            from  ..validators import paramater_validators
            self.validator = paramater_validators

        else:
            self.validator = validator

    def join_endpoint(self, item_id):
        return self.endpoint + '/' + item_id
