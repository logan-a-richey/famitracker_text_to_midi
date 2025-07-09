# generate_macro_key.py

def generate_macro_key(_inst_type: int, _macro_type: int, _macro_index: int):
    return "{}::{}::{}".format(_inst_type, _macro_type, _macro_index)
