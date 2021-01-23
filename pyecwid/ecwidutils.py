def get_attribute_json(attribute_id,value):
    return { 
        "attributes": [
            {
                "id": attribute_id,
                "value": value
            },
        ]
    }