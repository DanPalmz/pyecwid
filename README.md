# pyecwid
Python wrapper for Ecwid REST API
## Requirements
1. API token and Store ID from [Ecwid CP](https://my.ecwid.com/#develop-apps) Apps -> My Apps
2. Python 3
3. [Requests](https://pypi.org/project/requests/)
## Installation
```console
$ python -m pip install pyecwid
```
## ChangeLog
**BREAKING: Major changes (when 0.1.x released)**
* Broke up the different endpoints (Customers, Orders, Products, etc) into different classes that accept the EcwidAPI (or EcwidAPIMock) object.
* Added Mixins that can be used to quickly implement new Endpoints without duplicating code.
* Added an Ecwid class that contains properties with each endpoint initialised.
* Some methods have changed names.
## Todo
* Reimplement product_variations and other mixins for subobjects of items.

## Implemented Features ##
* Standard possible commands for endpoints:
    * add({item}) - add item (dict)
    * delete(id) - remove item
    * get_by_id(id) - get item details (returns a single {item})
    * update(id, {values}) - update item with values (dict)

    * **Getting multiple items**:  Will deal with pagination and return a list of "items" node.<br />*Optional: pass "collate_items=False" to any of these commands and full results will be returned.  Note - pagination will not be handled automatically.   Useful to find total counts etc.*
        * get() - get all items 
        * get_by_keyword('keyword') - search for items by keyword 
        * get_by_params({params}) - search for items by paramaters (dict)
    
| Endpoint | Status | Standard commands | Extra commands |
|---|---|---|---|
| Coupons |  _alpha - currently unable to test_ | add, delete, get, get_by_id, get_by_params, update | |
| Customers | _alpha - currently unable to test_ | add, delete, get, get_by_id, get_by_keyword, update | get_by_email, get_by_name |
| Orders |  _alpha - currently unable to test_ | add, delete, get, get_by_id, get_by_params, update | |
| Products | working | add, delete, get, get_by_id, get_by_keyword, get_by_params, update | |
| ProductTypes (classes) | working | add, delete, get, get_by_id, update | |


## Simple Initialisation
```python
from pyecwid import Ecwid
ecwid = Ecwid(api_token, store_id)
```
### EcwidAPI Arguments
| Argument | Required | Description | Default Value |
|---|---|---|---|
| api_token | Yes | The secret_ or public_ token for your store. | |
| store_id | Yes | The ID of your store. | |
| skip_test | No | True/False.  Skips test call to API during initiaization (used in tests) | False |
| base_url | No | Replace the hard coded URL <br />Note: format includes {0} for store_id | `'https://app.ecwid.com/api/v3/{0}/'` |

### Sample:  Search products and pprint
```python
from pprint import pprint
from pyecwid import Ecwid

ecwid = Ecwid('public_ASDF', '1234567')

# Search by Keyword
items = ecwid.products.get_by_keyword('sunglasses')
pprint(items)

# Search by Paramaters
params = { 'createdFrom': '2016-04-25', 'createdTo': '2020-12-25' }
items = ecwid.products.get_by_params(params)
pprint(items)

# Get all products and use lambda function to search results
items = ecwid.products.get()
usb_list = list(filter(lambda items: 'USB' in items.get('name'), items))
pprint(usb_list)

```
### Sample:  Add item (remove first if it exists) then modify details.
```python
from pyecwid import Ecwid
import json, time

ecwid = Ecwid('public_ASDF', '1234567')

# Import an item from JSON file
with open('./samplejson/product.json') as json_file:
    new_product = json.load(json_file)

# Check if item already exists.  If so remove.
product_search = ecwid.products.get_by_keyword(new_product['sku'])
if len(product_search) > 0:
    exisiting_item_id = product_search[0]['id']
    result = ecwid.products.delete(exisiting_item_id)
    if result == 1:
        print("Existing item removed")
        time.sleep(2)


new_item_id = ecwid.products.add(new_product)

updated_data = {'name': 'My New Product'}

result = ecwid.products.update(new_item_id, updated_data)
print(result.text)
```

### Sample: Just importing required endpoints
```python
from pyecwid import EcwidAPI
from pyecwid.endpoints import Products

API_TOKEN = 'secret_ASDF'
API_STORE = '1234567'

ecwid = EcwidAPI(API_TOKEN, API_STORE)
products = Products(ecwid)

results = products.get()
```
### Debugging: Use EcwidAPIMock for console logging calls.
```python
from pyecwid import EcwidMock

ecwid = EcwidMock(API_TOKEN, API_STORE)
result = ecwid.products.get()

```
OR
```python
from pyecwid import EcwidAPIMock
from pyecwid.endpoints import Products

ecwid = EcwidAPIMock(API_TOKEN, API_STORE)
products = Products(ecwid)

results = products.get()
```
