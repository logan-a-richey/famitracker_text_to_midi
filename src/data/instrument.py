# instrument.py

from typing import List
from helpers.constants import InstTypes
from data.macro_binding import MacroBinding

class InstBase:
    '''
    Instrument Base class.
    Contains `name` and `index` since those are common to all instruments.
    Contains __str__ and __repr__ methods to make all instruments printable types.
    '''

    def __init__(self, 
        _index: int, 
        _name: str
    ):
        self.index = _index
        self.name = _name
        self.inst_type = InstTypes.OTHER
    
    def __str__(self):
        ''' Make printable type '''
        return "<{}> {}".format(self.__class__.__name__, self.__dict__)
    
    def __repr__(self):
        return self.__str__()

class Inst2A03(InstBase):
    ''' 
    Data structure for 2A03 Instrument 
    Has Macros.
    Has KeyDPCM support.
    '''
    
    def __init__(self, 
        _index: int,
        _name: str,
        _seq_vol: int,
        _seq_arp: int,
        _seq_pit: int,
        _seq_hpi: int,
        _seq_wav: int
    ):
        super().__init__(_index, _name)
        self.macros = MacroBinding(_seq_vol, _seq_arp, _seq_pit, _seq_hpi, _seq_wav)
        self.key_dpcm = {}
        self.inst_type = InstTypes.INST_2A03

class InstVRC6(InstBase):
    ''' 
    Data structure for VRC6 Instrument 
    Has Macros.

    In more recent versions of FamiTracker, VRC6 can also include KeyDPCM.
    For strictness and compliance with official FamiTracker, I have left it out.
    '''

    def __init__(self, 
        _index: int,
        _name: str,
        _seq_vol: int,
        _seq_arp: int,
        _seq_pit: int,
        _seq_hpi: int,
        _seq_wav: int,
    ):
        super().__init__(_index, _name)
        self.macros = MacroBinding(_seq_vol, _seq_arp, _seq_pit, _seq_hpi, _seq_wav)
        self.inst_type = InstTypes.INST_VRC6

class InstN163(InstBase):
    ''' 
    Data structure for Namco Instrument 
    Has Macros.
    Has additional Namco settings.
    '''

    def __init__(self, 
        _index: int,
        _name: str,
        _seq_vol: int,
        _seq_arp: int,
        _seq_pit: int,
        _seq_hpi: int,
        _seq_wav: int,
        _w_size: int,
        _w_pos: int,
        _w_count: int
    ):
        super().__init__(_index, _name)
        self.macros = MacroBinding(_seq_vol, _seq_arp, _seq_pit, _seq_hpi, _seq_wav)
        self.w_size = _w_size
        self.w_pos = _w_pos
        self.w_count = _w_count
        self.waves = {}
        self.inst_type = InstTypes.INST_N163

class InstVRC7(InstBase):
    ''' 
    Data structure for FM Instrument 
    Has additional FM data such as patch and registers. 
    These control the frequency modulation of the instrument.
    '''
    
    def __init__(self,
        _index: int,
        _name: str,
        _patch: int,
        _registers: List[int]
    ):
        super().__init__(_index, _name)
        self.patch = _patch
        self.registers = _registers
        self.inst_type = InstTypes.INST_VRC7 
    
class InstS5B(InstBase):
    ''' 
    Data structure for Sunsoft Instrument 
    Has Macros.
    Sunsoft instrument is unique since it can also behave as a Noise instrument. 
    This is determined by Macros. 
    
    Since the Macro needed to be compliant with 2A03 and others, 
    the authors of FamiTracker used some 2's compliment magic to denote the state of S5B instruments.
    This information should be included in the MacroBinding object.
    '''

    def __init__(self,
        _index: int,
        _name: str,
        _seq_vol: int,
        _seq_arp: int,
        _seq_pit: int,
        _seq_hpi: int,
        _seq_wav: int,
    ):
        super().__init__(_index, _name)
        self.macros = MacroBinding(_seq_vol, _seq_arp, _seq_pit, _seq_hpi, _seq_wav)
        self.inst_type = InstTypes.INST_S5B

class InstFDS(InstBase):
    ''' 
    Data structure for FDS wavetable Instrument.
    
    Has Macros. (Note that FDS should not have HPI or DUT macros)
    Does not have a MacroBinding object attached for this reason.
    Macros are attached individually.

    Has additional FDS information such as fds_wave and fds_mod.
    '''

    def __init__(self,
        _index: int,
        _name: str,
        _mod_enable: int, 
        _mod_speed: int,
        _mod_depth: int,
        _mod_delay: int 
    ):
        super().__init__(_index, _name)
        self.mod_enable = _mod_enable
        self.mod_speed = _mod_speed
        self.mod_depth = _mod_depth
        self.mod_delay = _mod_delay

        self.fds_wave = []
        self.fds_mod = []

        self.mac_vol = None
        self.mac_arp = None
        self.mac_pit = None

        self.inst_type = InstTypes.INST_FDS
