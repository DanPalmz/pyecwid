# pyecwid
Python wrapper for Ecwid REST API

## Requirements
1. See requirements.txt
2. API token and Store ID from [Ecwid CP](https://my.ecwid.com/) Apps -> My Apps

## Implemented Features ##
* Product
    * product(id) - get product details
    * product_combinations(id) - get all combinations for a product
* Products
    * products() - return all products
    * products_by_keyword('keyword')
    * products_by_params({dict of search paramaters})
* Product types (classes)
    * product_classes() - return all configured product types in the store

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
### More advanced processing ###
Functions for client side processing of the data returned by the EcwidAPI class have been included in ecwidutils.py.  Look under [samples](./samples/) for usage.