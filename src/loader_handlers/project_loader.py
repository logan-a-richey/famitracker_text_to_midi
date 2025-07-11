# project_loader.py

import re
from typing import Optional, Dict, List, Callable 

# from helpers.constants import MacroTypes, InstTypes 
# from helpers.helper_functions import generate_macro_key 

from data.macro import Macro 
from data.instrument import Inst2A03, InstVRC6, InstVRC7, InstFDS, InstN163, InstS5B
from data.track import Track

from loader_handlers.info_handler import InfoHandler
from loader_handlers.macro_handler import MacroHandler
from loader_handlers.instrument_handler import InstrumentHandler
from loader_handlers.track_handler import TrackHandler
from loader_handlers.dpcm_handler import DPCMHandler
from loader_handlers.groove_handler import GrooveHandler
from loader_handlers.special_handler import SpecialHandler

from loader_handlers.handler_registry import collect_handlers

class ProjectLoader:
    def __init__(self):
        self.info_handler = InfoHandler()
        self.dpcm_handler = DPCMHandler()
        self.groove_handler = GrooveHandler()
        self.macro_handler = MacroHandler()
        self.instrument_handler = InstrumentHandler()
        self.special_handler = SpecialHandler()
        self.track_handler = TrackHandler()

        self.dispatch: Dict[str, callable] = {}
        self._load_dispatch()

    def _load_dispatch(self):
        for handler in [
            self.info_handler,
            self.dpcm_handler,
            self.groove_handler,
            self.macro_handler,
            self.instrument_handler,
            self.special_handler,
            self.track_handler
        ]:
            self.dispatch.update(collect_handlers(handler))       

    def load_project(self, project, input_file) -> None:
        # TODO better exception handling
        #try:
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == '#':
                    continue
                
                first_word = line.split()[0]
                handle = self.dispatch.get(first_word, None)
                if not handle:
                    print("[W] Did not handle: {}".format(line))
                    continue
                
                # print(first_word)
                handle(project, line)
            
        #except Exception as e:
        #    # for file not open error
        #    print("[E] {}".format(e))
        #    exit(1)
    
