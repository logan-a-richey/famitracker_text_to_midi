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
    MACRO = re.compile(r'''
        (?P<tag>\w+)\s+        
        (?P<type>\-?\d+)\s+     
        (?P<index>\-?\d+)\s+     
        (?P<loop>\-?\d+)\s+     
        (?P<release>\-?\d+)\s+     
        (?P<setting>\-?\d+)        
        \s*\:\s*
        (?P<data>.*)            
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
    INT_LIST = re.compile(r'\-?\d+')
    HEX_LIST = re.compile(r'[0-9A-F]{2}')
