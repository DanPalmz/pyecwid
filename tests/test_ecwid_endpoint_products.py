import json
import os
#from pprint import pprint
from pyecwid import Ecwid, EcwidMock
import pytest
import pytest_dependency
import pytest_dotenv
import time

API_TOKEN = os.getenv("API_TOKEN")
API_STORE = os.getenv("API_STORE")

SLEEP_TIME = 5

@pytest.fixture
def dummy_product():
    with open('./tests/samplejson/product.json') as json_file:
        return json.load(json_file)


@pytest.fixture
def dummy_product_id(dummy_product, live_ecwid):
    dummy_product_sku = dummy_product['sku']
    product_search = live_ecwid.products.get_by_keyword(dummy_product_sku)
    if len(product_search) > 0:
        return product_search[0]['id']


@pytest.fixture
def mock_ecwid():
    return EcwidMock(API_TOKEN, API_STORE)


@pytest.fixture
def live_ecwid():
    return Ecwid(API_TOKEN, API_STORE)


def test_product_malformed_id_raises_error(mock_ecwid):
    with pytest.raises(Exception, match='item_id not a valid number') as e:
        result = mock_ecwid.products.get_by_id('id1234')
        assert e.type is ValueError


# def test_product_variations_malformed_id_raises_error(mock_ecwid):
#     with pytest.raises(Exception, match='item_id not a valid number') as e:
#         result = mock_ecwid.product_variations('id1234')
#         assert e.type is ValueError


# def test_product_variation_update_malformed_id_raises_error(mock_ecwid):
#     with pytest.raises(Exception, match='item_id not a valid number') as e:
#         result = mock_ecwid.product_variation_update('abc1234', '1234', {'value': 'value'})
#         assert e.type is ValueError


# def test_product_variation_update_malformed_variation_id_raises_error(mock_ecwid):
#     with pytest.raises(Exception, match='variation_id not a valid number') as e:
#         result = mock_ecwid.product_variation_update('1234', 12.234, {'value': 'value'})
#         assert e.type is ValueError


# def test_product_variation_update_empty_values_raises_error(mock_ecwid):
#     with pytest.raises(Exception, match='Dictionary paramater should not be empty') as e:
#         result = mock_ecwid.product_variation_update('1234', '1234', {})
#         assert e.type is ValueError


# def test_product_variation_update_wrong_paramater_type_raises_error(mock_ecwid):
#     with pytest.raises(Exception, match='Paramater must be a valid dictionary') as e:
#         result = mock_ecwid.product_variation_update('1234', '1234', ['test'])
#         assert e.type is ValueError


def test_product_add_empty_dict_raises_errors(mock_ecwid):
    product = {}
    with pytest.raises(Exception, match='Dictionary paramater should not be empty') as e:
        result = mock_ecwid.products.add(product)
        assert e.type is ValueError


def test_product_update_malformed_id_raises_errors(mock_ecwid):
    product = {}
    with pytest.raises(Exception, match='item_id not a valid number') as e:
        result = mock_ecwid.products.update('id1234', product)
        assert e.type is ValueError


def test_product_update_empty_dict_raises_errors(mock_ecwid):
    product = {}
    with pytest.raises(Exception, match='Dictionary paramater should not be empty') as e:
        result = mock_ecwid.products.update('1234', product)
        assert e.type is ValueError


@pytest.mark.dependency()
def test_products_retrieves_products(live_ecwid):
    result = live_ecwid.products.get()
    assert len(result) > 1


@pytest.mark.dependency(depends=["test_products_retrieves_products"])
def test_product_remove_dummy_data_if_necessary(live_ecwid, dummy_product, dummy_product_id):
    if dummy_product_id:
        result = live_ecwid.products.delete(dummy_product_id)
        assert result == 1, "1 item removed"
    else:
        pass


@pytest.mark.dependency(depends=["test_product_remove_dummy_data_if_necessary"])
def test_product_add_dummy_data(live_ecwid, dummy_product):
    result = live_ecwid.products.add(dummy_product)

    # Sleep:  Server wasn't updating quick enough for tests following this one..
    time.sleep(SLEEP_TIME)
    assert isinstance(result, int)


@pytest.mark.dependency(depends=["test_product_add_dummy_data"])
def test_product_update_changes_values(live_ecwid, dummy_product_id):

    updated_data = {
        'name': 'Name set at {0}'.format(time.strftime("%H:%M:%S", time.localtime()))
    }
    update_result = live_ecwid.products.update(dummy_product_id, updated_data)

    confirm_name_updated = live_ecwid.products.get_by_id(dummy_product_id)['name']
    assert confirm_name_updated == updated_data['name']

def test_product_teardown(live_ecwid, dummy_product_id):
    if dummy_product_id:
        result = live_ecwid.products.delete(dummy_product_id)
        assert result == 1, "1 item removed"
    else:
        pass