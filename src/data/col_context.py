# col_context.py

class NoteData:
    ''' Information about the column state '''

    def __init__(self,
        _start: int,
        _pitch: int,
        _instrument: int,
        _volume: int
    ):
        # store fami note information
        self.start = _start
        self.pitch = _pitch 
        self.instrument = _instrument 
        self.volume = _volume 

        # store effect values
        self.arp_x = 0 
        self.arp_y = 0 
    
    def __str__(self):
        return "<{}> {}".format(self.__class__.__name__, self.__dict__)

    def __repr__(self):
        return self.__str__()
    

class ColContext:
    ''' 
    Contains buffered note data 
    Used to store intermediate note data in MidiExport.
    
    NoteData contains information about the column state.
    
    ColContext contains two NoteData objects
    context.curr contains the current data 
    context.last contains the cached data
    '''

    def __init__(self, _idx: int):
        self.idx = _idx
        self.is_playing = False
        
        self.curr = NoteData(0, 0, 0, 15)
        self.last = NoteData(0, 0, 0, 15)
        
        # ensure that a context can only add a note once per loop iteration
        self.one_shot = True

    def __str__(self):
        return "<{}> {}".format(self.__class__.__name__, self.__dict__)

    def __repr__(self):
        return self.__str__()
