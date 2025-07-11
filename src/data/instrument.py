# instrument.py

from typing import List
from helpers.inst_types import InstTypes

class MacroBinding:
    ''' Macro information for Instruments '''
    def __init__(self,
        _seq_vol: int,
        _seq_arp: int,
        _seq_pit: int,
        _seq_hpi: int,
        _seq_dut: int,
    ):
        self.seq_vol = _seq_vol 
        self.seq_arp = _seq_arp 
        self.seq_pit = _seq_pit 
        self.seq_hpi = _seq_hpi 
        self.seq_dut = _seq_dut 

        # populate with macro objects later
        self.mac_vol = None
        self.mac_arp = None
        self.mac_pit = None
        self.mac_hpi = None
        self.mac_dut = None
        
class InstBase:
    def __init__(self, 
        _index: int, 
        _name: str
    ):
        self.index = _index
        self.name = _name
        self.inst_type = InstTypes.Unknown

class Inst2A03(InstBase):
    ''' Data structure for 2A03 Instrument '''
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
        self.inst_type = InstTypes.Inst2A03

class InstVRC6(InstBase):
    ''' Data structure for VRC6 Instrument '''
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
        self.inst_type = InstTypes.InstVRC6

class InstN163(InstBase):
    ''' Data structure for Namco Instrument '''
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
        self.inst_type = InstTypes.InstN163

class InstVRC7(InstBase):
    ''' Data structure for FM Instrument '''
    def __init__(self,
        _index: int,
        _name: str,
        _patch: int,
        _registers: List[int]
    ):
        super().__init__(_index, _name)
        self.patch = _patch
        self.registers = _registers
        self.inst_type = InstTypes.InstVRC7
    
class InstS5B(InstBase):
    ''' Data structure for Sunsoft Instrument '''
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
        self.inst_type = InstTypes.InstS5B

class InstFDS(InstBase):
    ''' Data structure for FDS wavetable Instrument '''
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
        self.mac_hpi = None

        self.inst_type = InstTypes.InstFDS
