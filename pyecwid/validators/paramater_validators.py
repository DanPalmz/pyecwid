from collections.abc import Mapping

def get_str_of_value_or_false(item):
    ''' Sanity check.
    * Returns a string if int.
    * Checks a string is intable.
    * Returns false otherwise.
    '''
    if type(item) == int:
        item = str(item)
        return item
    elif type(item) == str:
        try:
            int(item)
            return item
        except ValueError:
            return False
    else:
        return False

def check_paramater_is_valid_dict(item):
    if not isinstance(item, Mapping):
        raise ValueError("Paramater must be a valid dictionary")
    elif len(item) == 0:
        raise ValueError("Dictionary paramater should not be empty")

    return True