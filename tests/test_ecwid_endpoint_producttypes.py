import json
import os
import pprint
from pyecwid import Ecwid, EcwidMock
import pytest
import pytest_dependency
import pytest_dotenv
import time

API_TOKEN = os.getenv("API_TOKEN")
API_STORE = os.getenv("API_STORE")

SLEEP_TIME = 5

@pytest.fixture
def live_ecwid():
    return Ecwid(API_TOKEN, API_STORE)

@pytest.fixture
def dummy_producttype():
    with open('./tests/samplejson/producttype.json') as json_file:
        return json.load(json_file)


@pytest.fixture
def dummy_producttype_id(dummy_producttype, live_ecwid):
    dummy_producttype_name = dummy_producttype['name']
    search = live_ecwid.producttypes.get()
    for pt in search:
        if pt.get('name') == dummy_producttype_name:
            return pt['id']

    return False


@pytest.mark.dependency()
def test_producttypes_retrieves_at_least_one_product_class(live_ecwid):
    result = live_ecwid.producttypes.get()
    assert len(result) >= 1


@pytest.mark.dependency(depends=["test_producttypes_retrieves_at_least_one_product_class"])
def test_producttypes_can_get_producttype_by_id(live_ecwid):
    pts = live_ecwid.producttypes.get()
    pt = pts[0]
    
    result = live_ecwid.producttypes.get_by_id(pt['id'])
    
    assert result['attributes'] == pt['attributes']
    

@pytest.mark.dependency(depends=["test_producttypes_retrieves_at_least_one_product_class"])
def test_producttype_remove_dummy_data_if_necessary(live_ecwid, dummy_producttype, dummy_producttype_id):
    if dummy_producttype_id:
        result = live_ecwid.producttypes.delete(dummy_producttype_id)
        assert result == 1, "1 item removed"
    else:
        pass

@pytest.mark.dependency(depends=["test_producttype_remove_dummy_data_if_necessary"])
def test_producttype_add_dummy_data(live_ecwid, dummy_producttype):
    result = live_ecwid.producttypes.add(dummy_producttype)

    # Sleep:  Server wasn't updating quick enough for tests following this one..
    time.sleep(SLEEP_TIME)
    print(result)
    assert isinstance(result, int)


@pytest.mark.dependency(depends=["test_producttype_add_dummy_data"])
def test_product_update_changes_values(live_ecwid, dummy_producttype_id):

    updated_data = {
        "attributes": [
            {
                "name": "TestUpdate",
                "type": "CUSTOM",
                "show": "DESCR"
            }
        ] 
    }

    update_result = live_ecwid.producttypes.update(dummy_producttype_id, updated_data)

    items = live_ecwid.producttypes.get_by_id(dummy_producttype_id)['attributes']
    
    # Return a list of items with name "TestUpdate" if it exists.  We should only get our 1 updated item.
    item = list(filter(lambda items: 'TestUpdate' in items.get('name'), items))
    
    assert item[0]['name'] == "TestUpdate"

@pytest.mark.dependency(depends=["test_producttype_add_dummy_data"])
def test_producttype_teardown(live_ecwid, dummy_producttype_id):
    time.sleep(SLEEP_TIME)
    if dummy_producttype_id:
        result = live_ecwid.producttypes.delete(dummy_producttype_id)
        print(result)
        assert result == 1, "1 item removed"
    else:
        pass