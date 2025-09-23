# key_dpcm.py

class KeyDPCM:
    ''' 
    Information about what DPCM sample to trigger for midi_pitch while using inst_index.
    Attached to an Inst2A03 map where key = midi_pitch and val = KeyDPCM object.
    '''

    def __init__(self,
        _inst: int, # inst_index
        _octave: int,
        _note: int,
        _sample: int,
        _pitch: int,
        _loop: int,
        _loop_point: int,
        _delta: int,
    ):
        self.inst = _inst
        self.octave = _octave
        self.note = _note
        self.sample = _sample
        self.pitch = _pitch
        self.loop = _loop
        self.loop_point = _loop_point
        self.delta = _delta
    
    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
