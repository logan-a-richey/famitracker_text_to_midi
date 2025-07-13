# col_context.py

class ColContext:
    ''' 
    Contains buffered note data 
    Used to store intermediate note data in MidiExport.
    '''

    def __init__(self, _idx: int):
        self.idx = _idx

        self.is_playing = False
        
        self.last_tick = 0          # 0 or greater
        self.curr_tick = 0
        
        self.pitch = 60         # middle c

        self.curr_inst = 0     # default inst
        self.last_inst = 0
        
        self.curr_vol = 15      # default hex max
        self.last_vol = 15

        # For 0XY effect
        self.arp_x = 0
        self.arp_y = 0