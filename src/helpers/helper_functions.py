# helper_functions.py

import re

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

def clean_string(input_string, mode="Snake") -> str:
    ''' 
    Removes all non-alphanumeric chars from a string
    Converts to snake_case
    '''

    WORD_REGEX = re.compile(r'[a-zA-Z0-9]+') 
    if mode == "Pascal":
        word_list = WORD_REGEX.findall(input_string)
        word_list = [word.capitalize() for word in word_list]
        output_string = "".join(word_list)
        return output_string 
    else:
        word_list = WORD_REGEX.findall(input_string)
        word_list = [word.lower() for word in word_list]
        output_string = "_".join(word_list)
        return output_string 