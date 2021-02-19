from collections.abc import Mapping
import json
from pprint import pprint
import requests
import urllib.parse

#from urllib.request import urlopen
#from pyecwid.classes import *
#from types import SimpleNamespace

API_BASE_URL = 'https://app.ecwid.com/api/v3/{0}/'
API_PAGE_LIMIT = 100
DEBUG = False

class EcwidAPI:

    def __init__(self, api_token, store_id):
        if len(api_token) < 5:
            raise ValueError('api_token must be provided')
        self.api_token = api_token
        self.store_id = self.__get_str_of_value_or_false(store_id)
        #self.store_id = store_id
        self.base_url = API_BASE_URL.format(store_id)
        self.debug = DEBUG

    def get_base_url(self):
        return(self.base_url)

    def product_classes(self):
        '''Returns a List of Product types (as a dict)
        https://api-docs.ecwid.com/reference/product-types
        
        If no product classes are added this will return  1 item with
        an "attributes" field which contains the common fields "Brand",
        "UPC" and also custom attributes.
        '''
        result = self.__get_api_request('classes')
        return result


    def product_combinations(self,product_id):
        ''' Get all combinations for a product
            Returns: List[{combinations}]
        https://api-docs.ecwid.com/reference/products
        '''
        product_id = self.__get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)
        
        endpoint = 'products/' + product_id + '/combinations'
        #print(endpoint)
        result = self.__get_api_request(endpoint)
        return result

    def product(self,product_id):
        ''' Get product details
            Returns: {product}
        https://api-docs.ecwid.com/reference/products
        '''
        product_id = self.__get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)
        
        endpoint = 'products/' + product_id
        #print(endpoint)
        result = self.__get_api_request(endpoint)
        return result


    def product_add(self,product):
        ''' Adds a single product.
            Returns product_id
            Requires product to be a dict with valid product structure
        '''
        if not isinstance(product, Mapping):
            raise ValueError("product format not valid")
        elif len(product) == 0:
            raise ValueError("product should not be empty")

        result = self.__post_api_request('products',product)

        if result.status_code != 200:
            raise UserWarning("Prouct not created.", result.status_code, result.text)

        return result.json()['id']

    def product_delete(self,product_id):
        ''' Deletes a single product.
            Returns deleteCount int
        '''

        product_id = self.__get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)
        else:
            endpoint = 'products/' + product_id

        result = self.__delete_api_request(endpoint)

        if result.status_code != 200:
            raise UserWarning("Product not deleted.", result.status_code, result.text)

        return result.json()['deleteCount']



    def product_update(self,product_id,values):
        ''' Update a single product.
            Requires values to update in dict
        '''
        product_id = self.__get_str_of_value_or_false(product_id)
        if not product_id:
            raise ValueError("product_id not a valid number", product_id)
            
        else:
            endpoint = 'products/' + product_id

        if not isinstance(values, Mapping):
            raise ValueError("values format not valid")
        elif len(values) == 0:
            raise ValueError("values should not be empty")

        result = self.__put_api_request(endpoint,values)
        return result 

    def products(self):
        ''' Search for all products
            Returns: List[{product},{product}]
        https://api-docs.ecwid.com/reference/products
        '''

        result = self.__get_api_request('products')
        return result
        
    def products_by_keyword(self,keyword):
        ''' Search products by keyword
            Returns: List[{product},{product}]
        https://api-docs.ecwid.com/reference/products
        '''
        params = { 'keyword': keyword }

        result = self.__get_api_request('products',params)
        return result 

    def products_by_params(self,params):
        ''' Here be dragons!
            Search products by paramaters specified in dict.
            Eg:  { 'keyword': 'dragons', 'updatedFrom': '2011-05-01' }
            Returns: List[{product},{product}]
        https://api-docs.ecwid.com/reference/products
        '''
        if type(params) != dict:
            return

        result = self.__get_api_request('products',params)
        return result 



    def __delete_api_request(self, endpoint):
        url = self.__get_feature_url(endpoint)
     
        payload = { 'token': self.api_token }
        result = requests.delete(url, params=payload)
        return result


    def __get_feature_url(self, endpoint):
        feature_url = urllib.parse.urljoin(self.base_url, endpoint)
        return feature_url


    def __get_api_request(self, endpoint, payload={}):
        feature_url = self.__get_feature_url(endpoint)

        payload['token'] =  self.api_token
        payload['limit'] = API_PAGE_LIMIT
        
        if self.__endpoint_paging(endpoint):
            if self.debug:
                print("Making request with paging ability")
            result = self.__paged_api_request(feature_url, payload, self.__endpoint_node(endpoint))
        else:
            result = self.__unpaged_api_request(feature_url, payload, self.__endpoint_node(endpoint))

        if self.debug:
            print ('Fetch returned: {0} Size: {1}'.format(type(result),len(result)))

        return result

    def __post_api_request(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        
        payload = { 'token': self.api_token }
        
        result = requests.post(url, params=payload, json=values)

        return result

    def __put_api_request(self, endpoint, values):
        url = self.__get_feature_url(endpoint)
        
        payload = { 'token': self.api_token }

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


    def __unpaged_api_request(self, url, payload, node):
        result = requests.get(url, params=payload).json()

        if node:
            result = result[node]

        return result

        
    def __paged_api_request(self, url, payload, node):
        total_items = int(requests.get(url, params=payload).json()['total'])

        #total_items = 100 #int(total_items) if total_items else 100
        if self.debug:
            print('Total items in request: {0}'.format(total_items))
            print('Collecting items from node: {0}'.format(node))
        all_items = []

        for offset in range(0, total_items, API_PAGE_LIMIT):
            payload['offset'] = offset
            #payload['limit'] = 100
            result = requests.get(url, params=payload).json()
            current_node = result.get(node)
            
            #print('My node type is: {0} Size: {1}'.format(type(current_node),len(current_node)))
            if self.debug:
                print('Processed offset {0} collected {1} items'.format(offset,len(current_node)))

            all_items += current_node
        
        return all_items

    # def __get(self, url, object_hook=None):
    #     with urlopen(url) as resource:
    #         return json.load(resource, object_hook=object_hook)

    def __get_str_of_value_or_false(self,item_id):
        ''' Sanity check.  
        * Returns a string if int.
        * Checks a string is intable.
        * Returns false otherwise.
        '''
        if type(item_id) == int:
            item_id = str(item_id)
            return item_id
        elif type(item_id) == str:
            try:
                int(item_id)
                return item_id
            except ValueError:
                return False
        else:
            return False
