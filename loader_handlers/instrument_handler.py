# instrument_handler.py

import re
from regex_patterns import RegexPatterns
from instrument import Inst2A03, InstVRC6, InstVRC7, InstN163, InstS5B, InstFDS

class InstrumentHandler:
    def __init__(self, parent):
        self.parent = parent
    
################################################################################
    @register("INST2A03")
    def handle_inst_2a03(self, project: "Project", line: str):
        regex_match = RegexPatterns.INST_2A03.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut"]
        inst_index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut = list(map(int, regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = Inst2A03(inst_index, inst_name, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut)
        
        # TODO
        # self.load_macro(inst_obj)
        
        project.instruments[inst_index] = inst_obj
    
################################################################################
    @register("INSTVRC6")
    def handle_inst_vrc6(self, project: "Project", line: str):
        regex_match = RegexPatterns.INST_VRC6.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut"]
        inst_index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut = list(map(int, regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = InstVRC6( inst_index, inst_name, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut)
        
        #TODO
        # self.load_macro(inst_obj)
        
        project.instruments[inst_index] = inst_obj
    
################################################################################
    @register("INSTVRC7")
    def handle_inst_vrc7(self, project: "Project", line: str):
        regex_match = RegexPatterns.INST_VRC7.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        inst_index, inst_patch = list(map(int, regex_match.group("index", "patch")))
        num_fields = ["r0", "r1", "r2", "r3", "r4", "r5", "r5", "r6", "r7"]
        inst_registers = list(map(int, regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = InstVRC7(inst_index, inst_name, inst_patch, inst_registers)
        
        project.instruments[inst_index] = inst_obj

################################################################################
    @register("INSTN163")
    def handle_inst_n163(self, project: "Project", line: str):
        ''' Namco instrument handler '''
        regex_match = RegexPatterns.INST_N163.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut", "w_size", "w_pos", "w_count", ]
        index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut, w_size, w_pos, w_count = \
            list(map(int, regex_match.group(*num_fields)))
        name = regex_match.group("name")

        inst_obj = InstN163(
            index, name, 
            seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut, 
            w_size, w_pos, w_count
        )
        self.load_macro(inst_obj)
        self.project.instruments[index] = inst_obj

################################################################################
    def parse_inst_fds(self, line) -> "InstFDS":
        pass

    @register("INSTFDS")
    def handle_inst_fds(self, project: "Project", line: str):
        ''' FDS Instrument handler '''
        regex_match = RegexPatterns.INST_FDS.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        num_fields = ["index", "mod_enable", "mod_speed", "mod_depth", "mod_delay"]

        index, mod_enable, mod_speed, mod_depth, mod_delay = \
            list(map(int, regex_match.group(*num_fields)))

        inst_obj = InstFDS()
        self.project.instruments[index] = inst_obj
        pass
        
    @register("INSTS5B")
    def handle_inst_s5b(self, project: "Project", line: str):
        ''' Sunsoft instrument handler '''
        regex_match = RegexPatterns.INST_2A03.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut"]
        inst_index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut = list(map(int, regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = InstS5B(inst_index, inst_name, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut)
        
        # TODO
        # self.load_macro(inst_obj)
        
        project.instruments[inst_index] = inst_obj

