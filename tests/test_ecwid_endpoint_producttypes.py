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

@pytest.fixture
def live_ecwid():
    return Ecwid(API_TOKEN, API_STORE)

def test_products_classes_retrieves_at_least_one_product_class(live_ecwid):
    result = live_ecwid.producttypes.get()
    assert len(result) >= 1
