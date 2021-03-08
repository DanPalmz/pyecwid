import requests
import urllib.parse
from pyecwid.validators import paramater_validators as validator

API_BASE_URL = 'https://app.ecwid.com/api/v3/{0}/'
API_PAGE_LIMIT = 100
DEBUG = False


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
        if not skip_test:
            self.__test_api_key()

    def get_base_url(self):
        return(self.base_url)

    def product_classes(self):
        '''Returns a List of Product types (as a dict)
        https://api-docs.ecwid.com/reference/product-types

        If no product classes are added this will return  1 item with
        an "attributes" field which contains the common fields "Brand",
        "UPC" and also custom attributes.
        '''
        result = self.__api_request_get('classes')
        return result

    def product(self, product_id):
        ''' Get product details
            Returns: {product}
        https://api-docs.ecwid.com/reference/products
        '''
        product_id = validator.get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)

        endpoint = 'products/' + product_id
        result = self.__api_request_get(endpoint)
        return result

    def product_add(self, product):
        ''' Adds a single product.
            Returns product_id
            Requires product to be a dict with valid product structure
        '''
        if not validator.check_paramater_is_valid_dict(product):
            return

        result = self.__api_request_post('products', product)

        if result.status_code != 200:
            raise UserWarning("Prouct not created.", result.status_code, result.text)

        return result.json()['id']

    def product_delete(self, product_id):
        ''' Deletes a single product.
            Returns deleteCount int
        '''

        product_id = validator.get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)
        else:
            endpoint = 'products/' + product_id

        result = self.__api_request_delete(endpoint)

        if result.status_code != 200:
            raise UserWarning("Product not deleted.", result.status_code, result.text)

        return result.json()['deleteCount']

    def product_update(self, product_id, values):
        ''' Update a single product.
            Requires values to update in dict
        '''
        product_id = validator.get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)
        else:
            endpoint = 'products/' + product_id

        if not validator.check_paramater_is_valid_dict(values):
            return

        result = self.__api_request_put(endpoint, values)
        return result

    def product_variations(self, product_id):
        ''' Get all variations/combinations for a product
            Returns: List[{combinations}]
        https://api-docs.ecwid.com/reference/products
        '''
        product_id = validator.get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)

        endpoint = 'products/' + product_id + '/combinations'
        result = self.__api_request_get(endpoint)
        return result

    def product_variation_update(self, product_id, varation_id, values):
        ''' Update a single variation/combination on a product.
            Requires values to update in dict
        '''
        product_id = validator.get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)

        varation_id = validator.get_str_of_value_or_false(varation_id)
        if not varation_id:
            raise ValueError("variation_id not a valid number", varation_id)

        if not validator.check_paramater_is_valid_dict(values):
            return

        endpoint = 'products/' + product_id + '/combinations/' + varation_id

        result = self.__api_request_put(endpoint, values)
        return result

    def products(self):
        ''' Search for all products
            Returns: List[{product},{product}]
        https://api-docs.ecwid.com/reference/products
        '''

        result = self.__api_request_get('products')
        return result

    def products_by_keyword(self, keyword):
        ''' Search products by keyword
            Returns: List[{product},{product}]
        https://api-docs.ecwid.com/reference/products
        '''
        params = {'keyword': keyword}

        result = self.__api_request_get('products', params)
        return result

    def products_by_params(self, params):
        ''' Here be dragons!
            Search products by paramaters specified in dict.
            Eg:  { 'keyword': 'dragons', 'updatedFrom': '2011-05-01' }
            Returns: List[{product},{product}]
        https://api-docs.ecwid.com/reference/products
        '''
        if type(params) != dict:
            return

        result = self.__api_request_get('products', params)
        return result

    def __api_request_delete(self, endpoint):
        url = self.__get_feature_url(endpoint)

        payload = {'token': self.api_token}
        result = requests.delete(url, params=payload)
        return result

    def __api_request_get(self, endpoint, payload={}):
        feature_url = self.__get_feature_url(endpoint)

        payload['token'] = self.api_token
        payload['limit'] = API_PAGE_LIMIT

        if self.__endpoint_paging(endpoint):
            if self.debug:
                print("Making request with paging ability")
            result = self.__api_request_get_paged(feature_url, payload, self.__endpoint_node(endpoint))
        else:
            result = self.__api_request_get_unpaged(feature_url, payload, self.__endpoint_node(endpoint))

        if self.debug:
            print('Fetch returned: {0} Size: {1}'.format(type(result), len(result)))

        return result

    def __api_request_get_paged(self, url, payload, node):
        items = requests.get(url, params=payload)

        total_items = int(self.__get_response_if_ok(items, json=True)['total'])
        # total_items = 100 #int(total_items) if total_items else 100
        if self.debug:
            print('Total items in request: {0}'.format(total_items))
            print('Collecting items from node: {0}'.format(node))
        all_items = []

        for offset in range(0, total_items, API_PAGE_LIMIT):
            payload['offset'] = offset
            # payload['limit'] = 100
            result = requests.get(url, params=payload)

            result = self.__get_response_if_ok(result, json=True)

            current_node = result.get(node)

            if self.debug:
                print('Processed offset {0} collected {1} items'.format(offset, len(current_node)))

            all_items += current_node
        return all_items

    def __api_request_get_unpaged(self, url, payload, node):
        result = requests.get(url, params=payload)
        result = self.__get_response_if_ok(result, json=True)
        if node:
            result = result[node]
        return result

    def __api_request_post(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        payload = {'token': self.api_token}
        result = requests.post(url, params=payload, json=values)
        return result

    def __api_request_put(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        payload = {'token': self.api_token}
        result = requests.put(url, params=payload, json=values)
        return result

    def __endpoint_node(self, endpoint):
        '''If we need the output from one node in an endpoints JSON return it here'''
        return {
            'products': 'items'
        }.get(endpoint, False)

    def __endpoint_paging(self, endpoint):
        '''If we need to use paging for an endpoint specify it here'''
        return {
            'products': True,
            'classes': False
        }.get(endpoint, False)

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
