import json
import os
from pprint import pprint
from pyecwid import EcwidAPI
import pytest
import pytest_dependency
import pytest_dotenv
import time

API_TOKEN = os.getenv("API_TOKEN")
API_STORE = os.getenv("API_STORE")

SLEEP_TIME = 5

@pytest.fixture
def test_ecwid():
    return EcwidAPI('public_1','my_store',skip_test=True)

@pytest.fixture
def live_ecwid():
    return EcwidAPI(API_TOKEN,API_STORE)

@pytest.fixture
def dummy_product():
    with open('./tests/samplejson/product.json') as json_file:
        return json.load(json_file)

@pytest.fixture
def dummy_product_id(dummy_product, live_ecwid):
    dummy_product_sku = dummy_product['sku']
    product_search = live_ecwid.products_by_keyword(dummy_product_sku)
    if len(product_search) > 0:
        return product_search[0]['id']

def test_ecwidapi_requires_token_is_string():
    with pytest.raises(Exception, match='api_token must be a valid string') as e:
        error_ecwid = EcwidAPI(123456,'12345')
        assert e.type is ValueError

def test_ecwidapi_requires_token_matches_public_or_secret():
    with pytest.raises(Exception, match='api_token must be a valid public or secret token string') as e:
        error_ecwid = EcwidAPI('blah_12345','12345')
        assert e.type is ValueError

def test_base_url(test_ecwid):
    """Tests our instance is created and can return the API URL correctly""" 
    base_url = test_ecwid.get_base_url()
    assert base_url == 'https://app.ecwid.com/api/v3/my_store/'


def test_product_malformed_id_raises_error(test_ecwid):
    with pytest.raises(Exception, match='product_id not a valid number') as e:
        result = test_ecwid.product('id1234')
        assert e.type is ValueError


def test_product_variations_malformed_id_raises_error(test_ecwid):
    with pytest.raises(Exception, match='product_id not a valid number') as e:
        result = test_ecwid.product_variations('id1234')
        assert e.type is ValueError


def test_product_variation_update_malformed_id_raises_error(test_ecwid):
    with pytest.raises(Exception, match='product_id not a valid number') as e:
        result = test_ecwid.product_variation_update('abc1234','1234',{ 'value': 'value'})
        assert e.type is ValueError

def test_product_variation_update_malformed_variation_id_raises_error(test_ecwid):
    with pytest.raises(Exception, match='variation_id not a valid number') as e:
        result = test_ecwid.product_variation_update('1234',12.234,{'value': 'value'})
        assert e.type is ValueError

def test_product_variation_update_empty_values_raises_error(test_ecwid):
    with pytest.raises(Exception, match='values should not be empty') as e:
        result = test_ecwid.product_variation_update('1234','1234',{})
        assert e.type is ValueError

def test_product_add_empty_dict_raises_errors(test_ecwid):
    product = {}
    with pytest.raises(Exception, match='product should not be empty') as e:
        result = test_ecwid.product_add(product)
        assert e.type is ValueError
        

def test_product_update_malformed_id_raises_errors(test_ecwid):
    product = {}
    with pytest.raises(Exception, match='product_id not a valid number') as e:
        result = test_ecwid.product_update('id1234', product)
        assert e.type is ValueError


def test_product_update_empty_dict_raises_errors(test_ecwid):
    product = {}
    with pytest.raises(Exception, match='values should not be empty') as e:
        result = test_ecwid.product_update('1234',product)
        assert e.type is ValueError

def test_products_classes_retrieves_at_least_one_product_class(live_ecwid):
    result = live_ecwid.product_classes()
    assert len(result) >= 1

@pytest.mark.dependency()
def test_products_retrieves_products(live_ecwid):
    result = live_ecwid.products()
    assert len(result) > 1


@pytest.mark.dependency(depends=["test_products_retrieves_products"])
def test_product_remove_dummy_data_if_necessary(live_ecwid, dummy_product, dummy_product_id):
    if dummy_product_id:
        result = live_ecwid.product_delete(dummy_product_id)
        assert result == 1, "1 item removed"
    else:
        pass

@pytest.mark.dependency(depends=["test_product_remove_dummy_data_if_necessary"])
def test_product_add_dummy_data(live_ecwid, dummy_product):
    result = live_ecwid.product_add(dummy_product)
    
    # Sleep:  Server wasn't updating quick enough for tests following this one..
    time.sleep(SLEEP_TIME)
    assert isinstance(result, int)
    
    

@pytest.mark.dependency(depends=["test_product_add_dummy_data"])
def test_product_update_changes_values(live_ecwid, dummy_product_id):

    updated_data = { 
        'name': 'Name set at {0}'.format(time.strftime("%H:%M:%S", time.localtime()))
    }
    update_result = live_ecwid.product_update(dummy_product_id, updated_data)

    confirm_name_updated = live_ecwid.product(dummy_product_id)['name']
    assert confirm_name_updated == updated_data['name']



