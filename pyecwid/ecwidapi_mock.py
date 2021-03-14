import urllib.parse
from pyecwid.validators import paramater_validators as validator

API_BASE_URL = 'https://ecwid.localhost/api/v3/{0}/'
API_PAGE_LIMIT = 100
DEBUG = True

class EcwidAPIMock:
    def __init__(self, api_token='secret_123', store_id='1234', skip_test=True, base_url=API_BASE_URL):
        if type(api_token) == str:
            if api_token.startswith(('secret_', 'public_')):
                self.api_token = api_token
            else:
                raise ValueError('api_token must be a valid public or secret token string')
        else:
            raise ValueError('api_token must be a valid string')

        self.store_id = validator.get_str_of_value_or_false(store_id)
        self.base_url = base_url.format(store_id)
        self.debug = DEBUG

    def get_request(self, endpoint, payload={}):
        feature_url = self.__get_feature_url(endpoint)

        payload['token'] = self.api_token
        payload['limit'] = API_PAGE_LIMIT

        print(f'Sending request to {feature_url} with {payload}')

    def get_base_url(self):
        return(self.base_url)

    def __get_feature_url(self, endpoint):
        feature_url = urllib.parse.urljoin(self.base_url, endpoint)
        return feature_url