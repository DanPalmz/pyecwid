import json
import os
from pprint import pprint
from pyecwid import Ecwid, EcwidMock
import pytest
import pytest_dependency
import pytest_dotenv
import time

API_TOKEN = os.getenv("API_TOKEN")
API_STORE = os.getenv("API_STORE")

SLEEP_TIME = 5

@pytest.fixture
def dummy_coupon():
    with open('./tests/samplejson/coupon.json') as json_file:
        return json.load(json_file)


@pytest.fixture
def dummy_coupon_id(dummy_coupon, live_ecwid):
    dummy_coupon_code = dummy_coupon['code']
    coupon_search = live_ecwid.coupons.get_by_params({'code': 'MOXQ3YCWXRXA'})

    if len(coupon_search) > 0:
        return coupon_search[0]['id']


@pytest.fixture
def live_ecwid():
    return Ecwid(API_TOKEN, API_STORE)


@pytest.mark.dependency()
def test_coupons_retrieves_coupons(live_ecwid):
    result = live_ecwid.coupons.get()
    assert len(result) > 1


@pytest.mark.dependency(depends=["test_coupons_retrieves_coupons"])
def test_coupon_remove_dummy_data_if_necessary(live_ecwid, dummy_coupon, dummy_coupon_id):
    if dummy_coupon_id:
        result = live_ecwid.coupons.delete(dummy_coupon_id)
        assert result == 1, "1 item removed"
    else:
        pass


@pytest.mark.dependency(depends=["test_coupon_remove_dummy_data_if_necessary"])
def test_coupon_add_dummy_customer(live_ecwid, dummy_coupon):
    result = live_ecwid.coupons.add(dummy_coupon)

    # Sleep:  Server wasn't updating quick enough for tests following this one..
    time.sleep(SLEEP_TIME)
    print(result)
    assert isinstance(result, int)