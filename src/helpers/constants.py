
class MacroTypes:
    VOL = 0
    ARP = 1 
    PIT = 2 
    HPI = 3  
    DUT = 4

class InstTypes:
    Unknown = -1
    Inst2A03 = 0
    InstVRC6 = 1
    InstVRC7 = 2
    InstFDS = 3
    InstN163 = 4
    InstS5B = 5
    InstMMC5 = 6

class TokenType:
    OTHER = 0           # ... .. .
    NOTE_ON = 1         # A-4 .. .
    NOTE_OFF = 2        # --- .. .
    NOTE_RELEASE = 3    # === .. .
    NOISE_ON = 4        # #-F .. .
    ECHO_BUFFER = 5     # ^-3 .. .

class ControlFlowType:
    OTHER = 0
    BXX = 1
    CXX = 2
    DXX = 3