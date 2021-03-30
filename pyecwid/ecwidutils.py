def get_attribute_json(attribute_id, value):
    return {
        "attributes": [
            {
                "id": attribute_id,
                "value": value
            },
        ]
    }


def exec_on_items(items, function_for_items, function_for_combinations):
    result = False
    for item in items:
        combinations = item.get('combinations')
        if len(combinations) > 0:
            func_result = function_for_combinations(combinations, item)
        else:
            func_result = function_for_items(item)

        if (func_result):
            if not result:
                result = func_result
            else:
                result += func_result

    return result
    