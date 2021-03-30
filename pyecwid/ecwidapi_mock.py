import urllib.parse
#import responses
from pyecwid.validators import paramater_validators as validator

API_BASE_URL = 'https://ecwid.localhost/api/v3/{0}/'
API_PAGE_LIMIT = 100
DEBUG = True

class EcwidAPIMock:
    def __init__(self, api_token='secret_123', store_id='1234', skip_test=True, base_url=API_BASE_URL):
        if isinstance(api_token, str):
            if api_token.startswith(('secret_', 'public_')):
                self.api_token = api_token
            else:
                raise ValueError('api_token must be a valid public or secret token string')
        else:
            raise ValueError('api_token must be a valid string')

        self.store_id = validator.get_str_of_value_or_false(store_id)
        self.base_url = base_url.format(store_id)
        self.debug = DEBUG


    def delete_request(self, endpoint):
        url = self.__get_feature_url(endpoint)

        payload = {'token': self.api_token}

        print(f'DELETE request: {url} with {payload}')

        result = RequestResult(200, {'deleteCount': 1})
        return result

    def get_request(self, endpoint, payload={}):
        feature_url = self.__get_feature_url(endpoint)

        payload['token'] = self.api_token
        payload['limit'] = API_PAGE_LIMIT

        print(f'GET request: {feature_url} with {payload}')

    def get_base_url(self):
        return(self.base_url)

    def post_request(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        payload = {'token': self.api_token}

        print(f'POST request: {url} with {payload}. \nValues:')
        print(values)

        result = RequestResult(200, {'id': 1234})
        return result

    def put_request(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        payload = {'token': self.api_token}

        print(f'PUT request: {url} with {payload}. \nValues:')
        print(values)

        result = RequestResult(200)
        return result

    def __get_feature_url(self, endpoint):
        feature_url = urllib.parse.urljoin(self.base_url, endpoint)
        return feature_url

class RequestResult:
    def __init__(self, result, json={}):
        self.status_code = result
        if json:
            self.json_value = json

    def json(self):
        return self.json_value
