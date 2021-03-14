import json
import os
#from pprint import pprint
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
    return EcwidAPI('public_1', 'my_store', skip_test=True)


@pytest.fixture
def live_ecwid():
    return EcwidAPI(API_TOKEN, API_STORE)


@pytest.fixture
def dummy_product():
    with open('./tests/samplejson/product.json') as json_file:
        return json.load(json_file)


def test_ecwidapi_requires_token_is_string():
    with pytest.raises(Exception, match='api_token must be a valid string') as e:
        error_ecwid = EcwidAPI(123456, '12345')
        assert e.type is ValueError


def test_ecwidapi_requires_token_matches_public_or_secret():
    with pytest.raises(Exception, match='api_token must be a valid public or secret token string') as e:
        error_ecwid = EcwidAPI('blah_12345', '12345')
        assert e.type is ValueError


def test_base_url(test_ecwid):
    """Tests our instance is created and can return the API URL correctly"""
    base_url = test_ecwid.get_base_url()
    assert base_url == 'https://app.ecwid.com/api/v3/my_store/'
