import urllib.parse
import requests
from pyecwid.validators import paramater_validators as validator

API_BASE_URL = 'https://app.ecwid.com/api/v3/{0}/'
API_PAGE_LIMIT = 100
DEBUG = False
ITEMS_NODE = 'items'

class EcwidAPI:
    """Python wrapper for Ecwid REST API.

    Usage Example:
        ::
            from pyecwid import EcwidAPI
            ecwid = EcwidAPI(api_token, store_id)
    Arguments:
        api_token:  The secret_ or public_ token for your store.
        store_id:   The ID of your store.
        skip_test:  Optional: skips test call to API during initiaization (used in tests)
        base_url:   Optional: Replace the hard coded URL
                        Note: format includes {0} for store_id
                        Eg: 'https://app.ecwid.com/api/v3/{0}/'
    """

    def __init__(self, api_token, store_id, skip_test=False, base_url=API_BASE_URL):
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
        if not skip_test:
            self.__test_api_key()

    def get_base_url(self):
        return self.base_url

    def delete_request(self, endpoint):
        url = self.__get_feature_url(endpoint)

        payload = {'token': self.api_token}
        result = requests.delete(url, params=payload)
        return result

    def get_request(self, endpoint, payload={}, collate_items=True):
        feature_url = self.__get_feature_url(endpoint)

        payload['token'] = self.api_token
        payload['limit'] = API_PAGE_LIMIT

        if collate_items:
            if self.debug:
                print("Making request with paging ability")
            result = self.__get_request_paged(feature_url, payload)
        else:
            result = self.__get_request_unpaged(feature_url, payload)

        if self.debug:
            print('Fetch returned: {0} Size: {1}'.format(type(result), len(result)))

        return result

    def __get_request_paged(self, url, payload):
        items = requests.get(url, params=payload)

        total_items = int(self.__get_response_if_ok(items, json=True)['total'])

        if self.debug:
            print(f"Total items in request: {total_items}")
            print(f"Collecting items from node: {ITEMS_NODE}")

        all_items = []

        for offset in range(0, total_items, API_PAGE_LIMIT):
            payload['offset'] = offset
            result = requests.get(url, params=payload)

            result = self.__get_response_if_ok(result, json=True)

            current_node = result.get(ITEMS_NODE)

            if self.debug:
                print('Processed offset {0} collected {1} items'.format(offset, len(current_node)))

            all_items += current_node
        return all_items

    def __get_request_unpaged(self, url, payload):
        result = requests.get(url, params=payload)
        result = self.__get_response_if_ok(result, json=True)
        return result

    def post_request(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        payload = {'token': self.api_token}
        result = requests.post(url, params=payload, json=values)
        return result

    def put_request(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        payload = {'token': self.api_token}
        result = requests.put(url, params=payload, json=values)
        return result

    def __get_feature_url(self, endpoint):
        feature_url = urllib.parse.urljoin(self.base_url, endpoint)
        return feature_url

    def __get_response_if_ok(self, response, json=False):
        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            if json:
                return response.json()
            else:
                return response
        else:
            response.raise_for_status()

    def __test_api_key(self):
        ''' Tests that the profile endpoint is available.
            This endpoint is available to all tokens with public_storefront scope
        '''
        url = self.__get_feature_url('profile')
        payload = {'token': self.api_token}

        result = requests.get(url, params=payload)
        result = self.__get_response_if_ok(result)
        return
