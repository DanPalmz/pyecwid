import requests
import json
import urllib.parse
from urllib.request import urlopen
from pprint import pprint
#from pyecwid.classes import *

#from types import SimpleNamespace

API_BASE_URL = 'https://app.ecwid.com/api/v3/{0}/'
API_PAGE_LIMIT = 100
DEBUG = False

class EcwidAPI:

    def __init__(self, api_token, store_id):
        self.api_token = api_token
        self.store_id = store_id
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
        
        #product_classes = []
        
        result = self.__get_api_request('classes')
        return result

        # for item in result:
        #     #pprint(item)
        #     p = ProductClass(**item)
        #     print('My item is {0}'.format(type(p)))    
        #     product_classes.append(p)
        
        # print('I have {0}'.format(len(product_classes)))
        # return product_classes

    def products(self):
        '''Returns a List containg the contents of /products "items"
        element (as a dict)
        https://api-docs.ecwid.com/reference/products
        '''

        #products = []

        result = self.__get_api_request('products')
        return result
        
        # for item in result:
        #     #pprint(item)
        #     p = Product(**item)
        #     #print('My item is {0}'.format(type(p)))    
        #     products.append(p)

        # print('I have {0}'.format(len(products)))
        


    def __get_feature_url(self, endpoint):
        feature_url = urllib.parse.urljoin(self.base_url, endpoint)
        return feature_url


    def __get_api_request(self, endpoint):
        feature_url = self.__get_feature_url(endpoint)

        payload = { 
            'token': self.api_token,
            'limit': API_PAGE_LIMIT }
        
        if self.__endpoint_paging(endpoint):
            if self.debug:
                print("Making request with paging ability")
            result = self.__paged_api_request(feature_url, payload, self.__endpoint_node(endpoint))
        else:
            result = self.__unpaged_api_request(feature_url, payload, self.__endpoint_node(endpoint))

        if self.debug:
            print ('Fetch returned: {0} Size: {1}'.format(type(result),len(result)))

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