# pyecwid
Python wrapper for Ecwid REST API

## Requirements
1. See requirements.txt
2. API token and Store ID from [Ecwid CP](https://my.ecwid.com/) Apps -> My Apps

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
