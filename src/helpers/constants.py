# constants.py

SUBDIVISION = 120 # 16th note

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