# track.py

from typing import List, Dict 

class Track:
    ''' 
    Contains Track state.
    Contains tokens, hashable ORDER substrings that can be accessed quickly.
    `self.lines` is a list of strings of sequential song data.
    '''
    
    count = 0

    def __init__(self):
        Track.count += 1
        self.index = Track.count

        self.name = ""
        self.speed = 6
        self.tempo = 150
        self.num_rows = 64
        self.num_cols = 5
        self.eff_cols = [1 for _ in range(5)]

        self.orders: Dict[int, List[int]] = {}
        self.tokens: Dict[any, str] = {}
        self.lines: List[str] = []

    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
