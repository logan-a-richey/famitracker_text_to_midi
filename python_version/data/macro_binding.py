# macro_binding.py

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

    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()