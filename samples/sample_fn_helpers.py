def print_item(item):
    print(item['name'])


def print_combinations(combinations, parent):
    for item in combinations:
        options = item.get('options')
        if len(options) == 1:
            print('--- {0} Name: {1} Value: {2}'.format(parent['name'], options[0]['name'], options[0]['value']))
        else:
            print('*** ERROR: Item {0} has {1} options'.format(parent['name'], len(options)))


def get_item_values(item):
    result = []
    if {'name', 'price', 'quantity', 'enabled'} <= item.keys():
        attributes = item.get('attributes')
        if len(attributes):
            attribute_set = attributes[0]

        item_dict = {
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'enabled': item['enabled'],
            'cost': attribute_set['value']
        }

        result.append(item_dict)

    return result


def get_combinations_values(combinations, parent):
    result = []
    for item in combinations:
        options = item.get('options')
        if len(options) == 1:
            print('--- {0} Name: {1} Value: {2}'.format(parent['name'], options[0]['name'], options[0]['value']))

            if {'sku', 'defaultDisplayedPrice', 'quantity'} <= item.keys():
                attributes = item.get('attributes')
                if len(attributes):
                    attribute_set = attributes[0]

                    item_dict = {
                        'name':     '{0} {1}'.format(parent['name'], item['sku']),
                        'price':    item['defaultDisplayedPrice'],
                        'quantity': item['quantity'],
                        'enabled':  parent['enabled'],
                        'cost':     attribute_set['value']
                    }
                    result.append(item_dict)
    return result


def do_nothing(_):
    pass


def do_nothing2(_1, _2):
    pass
