# macro.py

from typing import List 

class Macro:
    def __init__(self, 
        _type: int,
        _index: int, 
        _loop: int, 
        _release: int, 
        _setting: int, 
        _sequence: List[int]
    ):
        self.type = _type
        self.index = _index 
        self.loop = _loop
        self.release = _release
        self.setting = _setting
        self.sequence = _sequence
