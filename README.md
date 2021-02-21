# pyecwid
Python wrapper for Ecwid REST API
## Requirements
1. API token and Store ID from [Ecwid CP](https://my.ecwid.com/) Apps -> My Apps
2. Python 3
3. [Requests](https://pypi.org/project/requests/)
## Installation
```console
$ python -m pip install pyecwid
```
## Implemented Features - Product CRUD ##
* Product
    * product(id) - get product details
    * product_add(product) - add product (dict)
    * product_delete(id) - remove product
    * product_update(id, {values}) - update product with values (dict)
    * product_variations(product_id) - get all variations/combinations for a product
    * product_varation_update(product_id, variation_id, {values}) - update one item varation with values (dict)

* Products
    * products() - return all products
    * products_by_keyword('keyword') - search products for keyword
    * products_by_params({params}) - pass dict of paramaters to products API
 
* Product types (classes)
    * product_classes() - return all configured product types in the store

### Sample:  Search products for items matching keyword 'sunglasses'
```python
from pprint import pprint
from pyecwid import EcwidAPI

ecwid = EcwidAPI('public_ASDF','1234567')

items = ecwid.products_by_keyword('sunglasses')

pprint(items)
```
### Sample:  Return all products and create a list of items with 'USB' in the name.
```python
from pyecwid import EcwidAPI

API_TOKEN = 'secret_ASDF'
API_STORE = '1234567'

ecwid = EcwidAPI(API_TOKEN,API_STORE)

items = ecwid.products()
usb_list = list(filter(lambda items: 'USB' in items.get('name'), items))

pprint(usb_list)
```
### Sample:  Provide a paramater dict as search terms
```python
from pyecwid import EcwidAPI

API_TOKEN = 'secret_ASDF'
API_STORE = '1234567'

ecwid = EcwidAPI(API_TOKEN,API_STORE)

params = { 'createdFrom': '2016-04-25', 'createdTo': '2020-12-25' }

items = ecwid.products_by_params(params)

pprint(items)
```