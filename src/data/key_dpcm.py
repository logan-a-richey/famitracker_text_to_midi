# key_dpcm.py

class KeyDPCM:
    def __init__(self,
        inst: int,
        octave: int,
        note: int,
        sample: int,
        pitch: int,
        loop: int,
        loop_point: int,
        delta: int,
    ):
        self.inst = inst
        self.octave = octave
        self.note = note
        self.sample = sample
        self.pitch = pitch
        self.loop = loop
        self.loop_point = loop_point
        self.delta = delta
    
    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
