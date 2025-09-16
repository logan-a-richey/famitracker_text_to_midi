# track.py

from typing import List, Dict 

class Track:
    ''' 
    Contains Track state.
    Contains tokens, hashable ORDER substrings that can be accessed quickly.
    `self.lines` is a list of strings of sequential song data.
    '''
    
    count = 0

    def __init__(self,
        _num_rows: int,
        _speed: int,
        _tempo: int,
        _name: str
    ):
        Track.count += 1
        self.index = Track.count

        self.name = _name
        self.speed = _speed
        self.tempo = _tempo
        self.num_rows = _num_rows
        
        self.num_cols = 5
        self.eff_cols = [1 for _ in range(5)]

        self.orders: Dict[int, List[int]] = {}
        self.tokens: Dict[any, str] = {}
        self.lines: List[str] = []

        self.curr_speed = self.speed
        self.curr_tempo = self.tempo 

    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
