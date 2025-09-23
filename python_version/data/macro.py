# macro.py

from typing import List 

class Macro:
    ''' 
    Contains Macro information.
    A Macro contains an integer sequence that is activated at the start of a note.

    There are 5 types of Macro: VOL, ARP, PIT, HPI, and DUT.
    - VOL is the loudness of a note. 0 is silent and 15 is max.
    - ARP is the midi_pitch offset of a note. Has settings: 0=absolute, 1=fixed, 2=relative, 3=scheme
    - PIT is the fine tuning of a note.
    - HPI is the fine-tuning of a sound's pitch, specifically on the square wave channels, using the Pxx effect
    - DUT is the duty cycle (or wave setting) of an instrument.

    Difference between PIT and HPI (they both affect fine pitch but in different ways.)
    PIT offers a fine-grained, software-controlled adjustment to the pitch.
    HPI triggers a more specific, hardware-based sweep effect with unique characteristics 
    and limitations related to the NES sound chip's capabilities, usually with a logarithmic function.

    DUT can vary from instrument to instrument, depending on the number of waves available.
    For this reason, FamiTracker docs may refer to `dut` also as `wav` or `seq`.
    '''
    
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
