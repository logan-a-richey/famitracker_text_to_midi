# groove.py

from typing import List

class Groove:
    def __init__(self, 
        _index: int, 
        _size: int, 
        _data: List[int]
    ):
        self.index = _index 
        self.size = _size
        self.data = _data
    
    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
