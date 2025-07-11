# macro_handler.py

from helpers.regex_patterns import RegexPatterns

from helpers.constants import MacroTypes, InstTypes 
from helpers.helper_functions import generate_macro_key 

from data.macro import Macro 

from loader_handlers.handler_registry import register

class MacroHandler:
    def __init__(self):
        pass

    @register("MACRO")
    @register("MACROVRC6")
    @register("MACRON163")
    @register("MACROS5B")
    def handle_macro(self, project, line: str):
        ''' Macro handler '''
        regex_match = RegexPatterns.MACRO.match(line)

        macro_tag = regex_match.group("tag")
        
        num_fields = ["type", "index", "loop", "release", "setting"]
        macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(int, regex_match.group(*num_fields)))
        macro_seq = list(map(int, RegexPatterns.INT_LIST.findall(regex_match.group("data"))))
        
        inst_type = 0
        if macro_tag == "MACRO":
            inst_type == InstTypes.Inst2A03
        elif macro_tag == "MACROVRC6":
            inst_type = InstTypes.InstVRC6
        elif macro_tag == "MACRON163":
            inst_type = InstTypes.InstN163
        elif macro_tag == "MACROS5B":
            inst_type = InstTypes.InstS5B
        else:
            raise ValueError("Invalid Macro Type")
        
        macro_key = generate_macro_key(inst_type, macro_type, macro_index)
        macro_obj = Macro(macro_type, macro_index, macro_loop, macro_release, macro_setting, macro_seq, macro_key)
        project.macros[macro_key] = macro_obj
    
    # def load_macro(self, project: "Project", inst: "InstBase"):
    def load_macro(self, project, inst):
        inst_seq_indexes = [
            inst.macros.seq_vol, 
            inst.macros.seq_arp, 
            inst.macros.seq_pit, 
            inst.macros.seq_hpi, 
            inst.macros.seq_dut 
        ]
        macro_types = [
            MacroTypes.VOL, 
            MacroTypes.ARP, 
            MacroTypes.PIT, 
            MacroTypes.HPI, 
            MacroTypes.DUT
        ]
        inst_macro_fields = [
            inst.macros.mac_vol, 
            inst.macros.mac_arp, 
            inst.macros.mac_pit, 
            inst.macros.mac_hpi, 
            inst.macros.mac_dut
        ]
        for i in range(5):
            macro_key = generate_macro_key(inst.inst_type, macro_types[i], inst_seq_indexes[i])
            macro = project.macros.get(macro_key, None)
            if macro:
                inst_macro_fields[i] = macro
        
