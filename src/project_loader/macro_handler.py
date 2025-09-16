# macro_handler.py

from helpers.regex_patterns import RegexPatterns

from helpers.constants import MacroTypes, InstTypes 
from helpers.helper_functions import generate_macro_key 

from data.macro import Macro 

from project_loader.handler_registry import register

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
        if not regex_match:
            raise ValueError("{} Regex failed.".format(self.__class__.__name__))
        
        macro_tag = regex_match.group("tag")
        
        num_fields = ["type", "index", "loop", "release", "setting"]
        macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(int, regex_match.group(*num_fields)))
        macro_seq = list(map(int, RegexPatterns.INT_LIST.findall(regex_match.group("data"))))
        
        inst_type = 0
        if macro_tag == "MACRO":
            inst_type == InstTypes.INST_2A03
        elif macro_tag == "MACROVRC6":
            inst_type = InstTypes.INST_VRC6
        elif macro_tag == "MACRON163":
            inst_type = InstTypes.INST_N163
        elif macro_tag == "MACROS5B":
            inst_type = InstTypes.INST_S5B
        else:
            raise ValueError("Invalid Macro Type")
        
        macro_key = generate_macro_key(inst_type, macro_type, macro_index)
        macro_obj = Macro(macro_type, macro_index, macro_loop, macro_release, macro_setting, macro_seq, macro_key)
        project.macros[macro_key] = macro_obj
    
