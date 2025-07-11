# helper_functions.py

def generate_macro_key(_inst_type: int, _macro_type: int, _macro_index: int):
    ''' Used for macro token lookup during Project and Instrument creation and usage. '''
    # return "{}::{}::{}".format(_inst_type, _macro_type, _macro_index)
    return tuple([_inst_type, _macro_type, _macro_index])

def generate_token_key(pat, row, col):
    ''' Used for string token lookup during Track creation and usage. '''
    return tuple([pat, row, col])

def get_next_item(lst, item):
    ''' Get the next item of a list, given an item. Loop-around. '''
    if item not in lst:
        raise ValueError("Item not in list.")
    
    this_index = lst.index(item)
    next_index = (this_index + 1) % len(lst)
    return lst[next_index]
