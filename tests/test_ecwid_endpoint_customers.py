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
def dummy_customer():
    with open('./tests/samplejson/customer.json') as json_file:
        return json.load(json_file)


@pytest.fixture
def dummy_customer_id(dummy_customer, live_ecwid):
    dummy_customer_email = dummy_customer['email']
    customer_results = live_ecwid.customers.get_by_email(dummy_customer_email)
    
    if len(customer_results) > 0:
        return customer_results[0]['id']


@pytest.fixture
def live_ecwid():
    return Ecwid(API_TOKEN, API_STORE)

@pytest.mark.dependency()
def test_customers_retrieves_customers(live_ecwid):
    result = live_ecwid.customers.get()
    assert len(result) >= 1

@pytest.mark.dependency(depends=["test_customers_retrieves_customers"])
def test_product_remove_dummy_data_if_necessary(live_ecwid, dummy_customer, dummy_customer_id): 
    if dummy_customer_id:
        result = live_ecwid.customers.delete(dummy_customer_id)
        assert result == 1, "1 item removed"
    else:
        pass


@pytest.mark.dependency(depends=["test_product_remove_dummy_data_if_necessary"])
def test_customers_add_dummy_customer(live_ecwid, dummy_customer):
    result = live_ecwid.customers.add(dummy_customer)

    # Sleep:  Server wasn't updating quick enough for tests following this one..
    time.sleep(SLEEP_TIME)
    print(result)
    assert isinstance(result, int)
