# instrument_handler.py

import re
from helpers.macro_types import MacroTypes
from loader_handlers.handler_registry import register 
from helpers.regex_patterns import RegexPatterns
from data.instrument import Inst2A03, InstVRC6, InstVRC7, InstFDS, InstN163, InstS5B
from helpers.generate_macro_key import generate_macro_key

def load_macros(project, inst):
    """ Binds <Macro> from <Project> to <Instrument> if it exists. """
    macro_types = [
        MacroTypes.VOL, 
        MacroTypes.ARP, 
        MacroTypes.PIT, 
        MacroTypes.HPI, 
        MacroTypes.DUT
    ]
    inst_seq = [
        inst.macros.seq_vol, 
        inst.macros.seq_arp, 
        inst.macros.seq_pit, 
        inst.macros.seq_hpi, 
        inst.macros.seq_dut 
    ]
    inst_mac = [
        inst.macros.mac_vol, 
        inst.macros.mac_arp, 
        inst.macros.mac_pit, 
        inst.macros.mac_hpi, 
        inst.macros.mac_dut 
    ]
    for i in range(5):
        macro_key = generate_macro_key(inst.inst_type, macro_types[i], inst_seq[i])
        macro_obj = project.macros.get(macro_key, None)
        if not macro_obj:
            continue
        inst_mac[i] = macro_obj        

class InstrumentHandler:
    def __init__(self):
        pass

    @register("INST2A03")
    # def handle_inst_2a03(self, project: "Project", line: str):
    def handle_inst_2a03(self, project, line: str):
        regex_match = RegexPatterns.INST_BASIC.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut"]
        inst_index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut = list(map(int, regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = Inst2A03(inst_index, inst_name, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut)

        load_macros(project, inst_obj)

        project.instruments[inst_index] = inst_obj
    
    @register("INSTVRC6")
    # def handle_inst_vrc6(self, project: "Project", line: str):
    def handle_inst_vrc6(self, project, line: str):
        regex_match = RegexPatterns.INST_BASIC.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut"]
        inst_index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut = list(map(int, regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = InstVRC6( inst_index, inst_name, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut)
        
        load_macros(project, inst_obj)
        
        project.instruments[inst_index] = inst_obj
    
    @register("INSTVRC7")
    # def handle_inst_vrc7(self, project: "Project", line: str):
    def handle_inst_vrc7(self, project, line: str):
        regex_match = RegexPatterns.INST_VRC7.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        inst_index, inst_patch = list(map(int, regex_match.group("index", "patch")))
        num_fields = ["r0", "r1", "r2", "r3", "r4", "r5", "r5", "r6", "r7"]
        inst_registers = list(map(lambda x: int(x, 16), regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = InstVRC7(inst_index, inst_name, inst_patch, inst_registers)
        
        project.instruments[inst_index] = inst_obj

    @register("INSTN163")
    def handle_inst_n163(self, project,  line: str):
        """ Namco instrument handler """
        regex_match = RegexPatterns.INST_N163.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut", "w_size", "w_pos", "w_count"]
        index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut, w_size, w_pos, w_count = list(map(int, regex_match.group(*num_fields)))
        name = regex_match.group("name")

        inst_obj = InstN163( index, name, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut, w_size, w_pos, w_count)
        
        load_macros(project, inst_obj)
        
        project.instruments[index] = inst_obj

    @register("INSTFDS")
    # def handle_inst_fds(self, project: "Project", line: str):
    def handle_inst_fds(self, project, line: str):
        """ 
        FDS Instrument handler 
        Note that FDS is the only instrument in whichi Macros are added after instantiation 
        """
        regex_match = RegexPatterns.INST_FDS.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        num_fields = ["index", "mod_enable", "mod_speed", "mod_depth", "mod_delay"]

        index, mod_enable, mod_speed, mod_depth, mod_delay = \
            list(map(int, regex_match.group(*num_fields)))
        name = regex_match.group("name")

        inst_obj = InstFDS(index, name, mod_enable, mod_speed, mod_depth, mod_depth)
        project.instruments[index] = inst_obj

    @register("INSTS5B")
    # def handle_inst_s5b(self, project: "Project", line: str):
    def handle_inst_s5b(self, project, line: str):
        """ Sunsoft instrument handler """
        regex_match = RegexPatterns.INST_BASIC.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        inst_tag = regex_match.group("tag")
        num_fields = ["index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut"]
        inst_index, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut = list(map(int, regex_match.group(*num_fields)))
        inst_name = regex_match.group("name")
        
        inst_obj = InstS5B(inst_index, inst_name, seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut)
        
        load_macros(project, inst_obj)
        
        project.instruments[inst_index] = inst_obj
