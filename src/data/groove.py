# groove.py

from typing import List

class Groove:
    def __init__(self, index: int, size: int, data: List[int]):
        self.index = index 
        self.size = size
        self.data = data
    
    def __str__(self):
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
