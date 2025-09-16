# groove.py

from typing import List

class Groove:
    '''
    Contains information about a FamiTracker Groove.
    Data represents the FXX change from line to line.

    Example:
    data = [1, 2, 3, 4]

    # Without Groove:
    ROW 00 : C-4 .. . F01
    ROW 01 : D-4 .. . F02
    ROW 02 : E-4 .. . F03
    ROW 03 : F-4 .. . F04
    
    # Set groove to 1. We use capital 'O' since 'G' is taken from note_delay and 'R' for pitch_down.
    ROW 04 : C-4 .. . O01   # F01: 
    ROW 05 : D-4 .. . ...   # F02
    ROW 06 : E-4 .. . ...   # F03
    ROW 07 : F-4 .. . ...   # F04
    
    This allows the composer to easily modify swing settings with the FXX effect.
    '''

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
