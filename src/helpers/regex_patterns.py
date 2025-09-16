# regex_patterns.py

import re

class RegexPatterns:
    SONG_INFORMATION = re.compile(r'''
        ^(?P<tag>\w+)\s+        
        \"(?P<name>.*)\"        
        ''', re.VERBOSE)
    GLOBAL_SETTINGS = re.compile(r'''
        ^(?P<tag>\w+)\s+       
        (?P<value>\d+)           
        ''', re.VERBOSE)
    DPCM_DEF = re.compile(r'''
        ^(?P<tag>DPCMDEF)\s+
        (?P<index>\d+)\s+
        (?P<size>\d+)\s*
        \"(?P<name>.*)\"
        ''', re.VERBOSE)
    
    GROOVE = re.compile(r'''
        ^(?P<tag>GROOVE)\s+
        (?P<index>\d+)\s+
        (?P<size>\d+)\s*\:\s*
        (?P<data>.*)$
        ''', re.VERBOSE)

    MACRO = re.compile(r'''
        (?P<tag>\w+)\s+        
        (?P<type>\-?\d+)\s+     
        (?P<index>\-?\d+)\s+     
        (?P<loop>\-?\d+)\s+     
        (?P<release>\-?\d+)\s+     
        (?P<setting>\-?\d+)        
        \s*\:\s*
        (?P<data>.*)$            
        ''', re.VERBOSE)
    INST_BASIC = re.compile(r'''
        ^(?P<tag>\w+)\s+       
        (?P<index>\-?\d+)\s+     
        (?P<seq_vol>\-?\d+)\s+     
        (?P<seq_arp>\-?\d+)\s+     
        (?P<seq_pit>\-?\d+)\s+     
        (?P<seq_hpi>\-?\d+)\s+     
        (?P<seq_dut>\-?\d+)\s*     
        \"(?P<name>.*)\"        
        ''', re.VERBOSE)
    INST_VRC7 = re.compile(r'''
        ^(?P<tag>\w+)\s+           
        (?P<index>\-?\d+)\s+         
        (?P<patch>\-?\d+)\s+         
        (?P<r0>[0-9A-F]{2})\s+    
        (?P<r1>[0-9A-F]{2})\s+    
        (?P<r2>[0-9A-F]{2})\s+    
        (?P<r3>[0-9A-F]{2})\s+    
        (?P<r4>[0-9A-F]{2})\s+    
        (?P<r5>[0-9A-F]{2})\s+    
        (?P<r6>[0-9A-F]{2})\s+    
        (?P<r7>[0-9A-F]{2})\s*    
        \"(?P<name>.*)\"            
        ''', re.VERBOSE)
    INST_FDS = re.compile(r'''
        ^(?P<tag>\w+)\s+       
        (?P<index>\d+)\s+        
        (?P<mod_enable>\d+)\s+        
        (?P<mod_speed>\d+)\s+        
        (?P<mod_depth>\d+)\s+        
        (?P<mod_delay>\d+)\s*        
        \"(?P<name>.*)\"        
        ''', re.VERBOSE)
    INST_N163 = re.compile(r'''
        ^(?P<tag>\w+)\s+       
        (?P<index>\-?\d+)\s+     
        (?P<seq_vol>\-?\d+)\s+     
        (?P<seq_arp>\-?\d+)\s+     
        (?P<seq_pit>\-?\d+)\s+     
        (?P<seq_hpi>\-?\d+)\s+     
        (?P<seq_dut>\-?\d+)\s+     
        (?P<w_size>\d+)\s+        
        (?P<w_pos>\d+)\s+        
        (?P<w_count>\d+)\s*        
        \"(?P<name>.*)\"        
        ''', re.VERBOSE)
    KEY_DPCM = re.compile(r'''
        ^(?P<tag>KEYDPCM)\s+
        (?P<inst>\-?\d+)\s+
        (?P<octave>\-?\d+)\s+
        (?P<note>\-?\d+)\s+
        (?P<sample>\-?\d+)\s+
        (?P<pitch>\-?\d+)\s+
        (?P<loop>\-?\d+)\s+
        (?P<loop_point>\-?\d+)\s+
        (?P<delta>\-?\d+)
        ''', re.VERBOSE)
    FDS_MACRO = re.compile(r'''
        ^(?P<tag>FDSMACRO)\s+
        (?P<inst>\d+)\s+
        (?P<type>\d+)\s+
        (?P<loop>\-?\d+)\s+
        (?P<release>\-?\d+)\s+
        (?P<setting>\-?\d+)\s*\:\s*
        (?P<data>.*)$
        ''', re.VERBOSE)
    TRACK = re.compile(r'''
        ^(?P<tag>TRACK)\s+
        (?P<num_rows>\d+)\s+
        (?P<speed>\d+)\s+
        (?P<tempo>\d+)\s*
        \"(?P<name>.*)\"
        ''', re.VERBOSE)
    COLUMNS = re.compile(r'''
        ^(?P<tag>COLUMNS)
        \s*\:\s*
        (?P<data>.*)$
        ''', re.VERBOSE)
    ORDER = re.compile(r'''
        ^(?P<tag>ORDER)\s+
        (?P<frame>[0-9A-F]{2})
        \s*\:\s*
        (?P<data>.*)$
        ''', re.VERBOSE)
    PATTERN = re.compile(r'''
        ^(?P<tag>PATTERN)\s+
        (?P<val>[0-9A-F]{2})
        ''', re.VERBOSE)
    ROW = re.compile(r'''
        ^(?P<tag>ROW)\s+
        (?P<row>[0-9A-F]{2})
        \s*\:\s*
        (?P<data>.*)$
        ''', re.VERBOSE)
    
    INT_LIST = re.compile(r'\-?\d+')
    HEX_LIST = re.compile(r'[0-9A-F]{2}')

    NOTE_ON = re.compile(r'^[A-G][\-#b]\d')
    NOTE_OFF = re.compile(r'^\-{3}')
    NOTE_RELEASE = re.compile(r'^\={3}')
    NOISE_ON = re.compile(r'[0-9A-F]\-\#')
    ECHO_BUFFER = re.compile(r'^\^\-[0-3]')

    TOKEN_NOTE_ON = re.compile(r'^[A-G][\-#b][0-9]$')
    TOKEN_NOISE_ON = re.compile(r'^[0-9A-F]\-\#$')
    TOKEN_INST = re.compile(r'^[0-9A-F]{2}$')
    TOKEN_VOL = re.compile(r'^[0-9A-F]$')

    BXX = re.compile(r'B[0-9A-F]{2}')
    CXX = re.compile(r'C[0-9A-F]{2}')
    DXX = re.compile(r'D[0-9A-F]{2}')

    EFFECT_RQ = re.compile(r'[RQ][0-9A-F]{2}')
    EFFECT_ARP = re.compile(r'[0][0-9A-F]{2}')
    EFFECT_GXX = re.compile(r'[G][0-9A-F]{2}')
    EFFECT_SXX = re.compile(r'[S][0-09A-F]{2}')
    EFFECT_SPEED_AND_TEMPO = re.compile(r'F[0-9A-F]{2}')
