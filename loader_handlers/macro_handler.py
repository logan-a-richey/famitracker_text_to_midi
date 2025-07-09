# macro_handler.py

class MacroHandler:
    def __init__(self, parent):
        self.parent = parent

    def parse_macro(self, line: str):
        pass
    
    @register("MACRO")
    @register("MACROVRC6")
    @register("MACRON163")
    @register("MACROS5B")
    def handle_macro(self, line: str):
        ''' Macro handler '''
        regex_match = regex_patterns["MACRO"].match(line)

        macro_tag = regex_match.group("tag")
        
        num_fields = ["type", "index", "loop", "release", "setting"]
        macro_type, macro_index, macro_loop, macro_release, macro_setting = list(map(int, regex_match.group(*num_fields)))
        macro_data_str = regex_match.group("data")
        macro_seq = list(map(int, regex_patterns["INT_LIST"].findall(macro_data_str)))
        
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
            # invalid instrument macro type
            return
        
        macro_key = generate_macro_key(inst_type, macro_type, macro_index)
        macro_obj = Macro(macro_type, macro_index, macro_loop, macro_release, macro_setting, macro_seq)
        self.project.macros[macro_key] = macro_obj
    
    def load_macro(self, inst: "InstBase"):
        # load macros - I think we know all information ahead of time, 
        # but doing it this way since for FDS, we need to add Macro after instrument creation, not before.
        
        # TODO  zip these together?
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
            macro_key = generate_macro_key(
                inst.inst_type, 
                macro_types[i], 
                inst_seq_indexes[i]
            )
            macro = self.project.macros.get(macro_key, None)
            if macro:
                inst_macro_fields[i] = macro
        self.parse_macro(line)
        pass

