# special_handler.py

from loader_handlers.handler_registry import register

from data.key_dpcm import KeyDPCM
from data.macro import Macro 

from helpers.regex_patterns import RegexPatterns

from helpers.constants import MacroTypes, InstTypes 
from helpers.helper_functions import generate_macro_key 

class SpecialHandler:
    def __init__(self):
        pass

    @register("KEYDPCM")
    def handle_key_dpcm(self, project, line):
        regex_match = RegexPatterns.KEY_DPCM.match(line)
        if not regex_match:
            print(line)
            raise ValueError("Regex failed.")

        fields = [
            "inst",
            "octave",
            "note",
            "sample",
            "pitch",
            "loop",
            "loop_point",
            "delta"
        ] 
        inst_index, octave, note, sample, pitch, loop, loop_point, delta = list(map(int, regex_match.group(*fields)))
        key_dpcm_obj = KeyDPCM(inst_index, octave, note, sample, pitch, loop, loop_point, delta)
        
        inst_obj = project.instruments.get(inst_index, None)
        if not inst_obj:
            print("[W] Could not find inst_index {} in method key_dpcm".format(inst_index))
            return

        #if not inst.inst_type == InstTypes.Inst2A03:
        #    raise ValueError("Could not add KeyDPCM to non-2A03 instrument")
        
        if not hasattr(inst_obj, "key_dpcm"):
            print("[W] Inst object does not have attr \'key_dpcm\'")
            return
        
        note_pitch = octave * 12 + note
        inst_obj.key_dpcm[note_pitch] = key_dpcm_obj

    @register("FDSWAVE")
    def handle_fds_wave(self, project, line):
        inst_index = int(line.split()[1])
        num_field = line.split(":")[1].strip().split()
        lst = list(map(int, num_field))
        
        inst_lookup = project.instruments.get(inst_index)
        if not inst_lookup:
            return

        if not hasattr(inst_lookup, "fds_wave"):
            return

        inst_lookup.fds_wave = lst

    @register("FDSMOD")
    def handle_fds_wave(self, project, line):
        inst_index = int(line.split()[1])
        num_field = line.split(":")[1].strip().split()
        lst = list(map(int, num_field))
        
        inst_lookup = project.instruments.get(inst_index)
        if not inst_lookup:
            return

        if not hasattr(inst_lookup, "fds_mod"):
            return

        inst_lookup.fds_mod = lst
    
    @register("FDSMACRO")
    def handle_fds_macro(self, project, line):
        # FDSMACRO [inst] [type] [loop] [release] [setting] : [macro]
        regex_match = RegexPatterns.FDS_MACRO.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        fields = ["inst", "type", "loop", "release", "setting"]
        inst_index, macro_type, macro_loop, macro_release, macro_setting = list(map(
            int, 
            regex_match.group(*fields)
        ))

        macro_sequence = list(map(int, regex_match.group("lst")))
         
        # this value does not matter since it isn't added to Project macros
        # this macro is only binded to InstFDS 
        default_macro_index = 0
        
        macro_key = generate_macro_key(InstTypes.InstFDS, macro_type, default_macro_index)

        # TODO
        macro_obj = Macro(
            macro_type, 
            default_macro_index,
            macro_loop, 
            macro_release, 
            macro_setting,
            macro_sequence,
            macro_key
        )

        inst_lookup = project.instruments.get(inst_index)
        if not inst_lookup:
            return

        if macro_type == MacroTypes.VOL:
            inst_lookup.mac_vol = macro_obj
        elif macro_type == MacroTypes.ARP:
            inst_lookup.mac_arp = macro_obj
        elif macro_type == MacroTypes.PIT:
            inst_lookup.mac_pit = macro_obj
        else:
            return
