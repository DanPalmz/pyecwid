from pyecwid import EcwidAPI
import json
from pprint import pprint

TEST_API_TOKEN = ''
TEST_API_STORE = ''

def test_product_list():
    """Tests the API call to ensure products are returned"""
    pass

def test_base_url():
    """Tests our instance is created and can return the API URL correctly"""
    test_ecwid = EcwidAPI('my_token','my_store')
    base_url = test_ecwid.get_base_url()
    assert base_url == 'https://app.ecwid.com/api/v3/my_store/'

def test_products():
    test_ecwid = EcwidAPI(TEST_API_TOKEN,TEST_API_STORE)
    test_ecwid.debug = True
    result = test_ecwid.products()
    usb_list = list(filter(lambda result: 'USB' in result.get('name'), result))
    pprint(usb_list)
    assert usb_list[0]['id'] == 271343630

def test_products_classes():
    test_ecwid = EcwidAPI(TEST_API_TOKEN,TEST_API_STORE)
    result = test_ecwid.product_classes()
    attributes = result[0].get('attributes')
    #pprint(attributes)
    assert attributes[0]['type'] == 'UPC'


def test_current():
    """Whatever I'm testing"""
    #test_ecwid = EcwidAPI(TEST_API_TOKEN,TEST_API_STORE)
    #test_ecwid.debug = True

    #result = test_ecwid.product_classes()

    assert True


