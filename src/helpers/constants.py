# constants.py

class DrumMidiConstants:
    DRUM_TRACK = 0 
    DRUM_CHANNEL = 9
    DRUM_VOL = 120

class MacroTypes:
    VOL = 0
    ARP = 1 
    PIT = 2 
    HPI = 3  
    DUT = 4

class InstTypes:
    OTHER     = 0
    INST_2A03 = 1
    INST_VRC6 = 2
    INST_VRC7 = 3
    INST_FDS  = 4
    INST_N163 = 5
    INST_S5B  = 6
    INST_MMC5 = 7

class TokenType:
    OTHER        = 0 # ... .. .
    NOTE_ON      = 1 # A-4 .. .
    NOTE_OFF     = 2 # --- .. .
    NOTE_RELEASE = 3 # === .. .
    NOISE_ON     = 4 # #-F .. .
    ECHO_BUFFER  = 5 # ^-3 .. .

class ControlFlowType:
    OTHER   = 0
    BXX     = 1
    CXX     = 2
    DXX     = 3

class DrumPitches:
    BASS_DRUM = 35
    SNARE_RIM = 37
    SNARE_DRUM = 38 
    
    HI_HAT_CLOSED = 42 
    HI_HAT_OPEN = 46 
    # HI_HAT_FOOT = 44 

    CYM_CRASH = 49
    CYM_RIDE = 51 
    CYM_CHINA = 52
    CYM_SPLASH = 55

    TOM_LOW_FLOOR = 41
    TOM_HI_FLOOR = 43
    TOM_LOW = 45
    TOM_LOW_MID = 47
    TOM_HI_MID = 48 
    TOM_HI = 50

    COWBELL = 56
