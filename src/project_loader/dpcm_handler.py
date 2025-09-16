# dpcm_handler.py

from project_loader.handler_registry import register 
from helpers.regex_patterns import RegexPatterns
from data.dpcm import DPCM

class DPCMHandler:
    def __init__(self):
        self.dpcm_index = 0 
    
    @register("DPCMDEF")
    def handle_dpcm_def(self, project, line):
        '''
        DPCMDEF   0   289 "kick03.dmc"
        '''
        regex_match = RegexPatterns.DPCM_DEF.match(line)
        if not regex_match:
            raise ValueError("{} Regex failed.".format(self.__class__.__name__))
        
        index, size = list(map(int, regex_match.group("index", "size")))
        name = regex_match.group("name")

        self.dpcm_index = index 
        dpcm_obj = DPCM(index, size, name)
        project.dpcm[index] = dpcm_obj

    @register("DPCM")
    def handle_dpcm(self, project, line):
        '''
        DPCM : 00 12 FF FE E7 FF 9F F1 03 C0 00 02 00 08 81 70 9C F9 E7 3C FF FF FB FD FD 8F 71 12 0C 42 10 42
        '''
        my_dpcm = project.dpcm[self.dpcm_index]

        lst =  list(map(lambda x: int(x, 16), line.split(":")[1].strip().split()))
        my_dpcm.data.extend(lst)
