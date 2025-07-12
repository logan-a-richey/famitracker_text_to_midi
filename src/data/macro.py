# macro.py

from typing import List 

class Macro:
    def __init__(self, 
        _type: int,
        _index: int, 
        _loop: int, 
        _release: int, 
        _setting: int, 
        _sequence: List[int],
        _macro_key: any
    ):
        self.type = _type
        self.index = _index 
        self.loop = _loop
        self.release = _release
        self.setting = _setting
        self.sequence = _sequence
        self.macro_key = _macro_key
    
    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
