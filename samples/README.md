## Sample Files ##

### sample_fn_helpers.py ###
**Helper Functions for use with ecwidutils.exec_on_items()**

Duplicate / customise these functions to implement functionality when looping over a set of items (namely products).

#### ecwidutils.exec_on_items ####
|paramater    |type  |description    |
|---------|---------|---------|
|items|list|the list of items (proucts) to be processed|
|function_for_items|function|function called when item has no combinations|
|function_for_combinations|function|function called when item has combinations|

#### Sample Code ####
```python
from pyecwid import EcwidAPI, ecwidutils
from samples import sample_fn_helpers

API_TOKEN = 'secret_ASDF'
API_STORE = '1234567'

ecwid = EcwidAPI(API_TOKEN,API_STORE)

items = ecwid.products()

# Simple print name etc #
results = ecwidutils.exec_on_items(items, 
    sample_fn_helpers.print_item, 
    sample_fn_helpers.print_combinations)

# Get details of product pricing, enabled status, combinations, quantity etc # 
stock_items = ecwidutils.exec_on_items(items,
    sample_fn_helpers.get_item_values,
    sample_fn_helpers.get_combinations_values)

```