# project_loader.py

import re
from typing import Optional, Dict, List, Callable 

from helpers.macro_types import MacroTypes 
from helpers.inst_types import InstTypes
from helpers.generate_macro_key import generate_macro_key

from data.macro import Macro 
from data.instrument import Inst2A03, InstVRC6, InstVRC7, InstFDS, InstN163, InstS5B
from data.track import Track

from loader_handlers.info_handler import InfoHandler
from loader_handlers.macro_handler import MacroHandler
from loader_handlers.instrument_handler import InstrumentHandler
from loader_handlers.track_handler import TrackHandler

from loader_handlers.handler_registry import collect_handlers

class ProjectLoader:
    def __init__(self):
        self.project = None
        self.current_pattern: int = 0
        
        self.info_handler = InfoHandler(self)
        self.macro_handler = MacroHandler(self)
        self.instrument_handler = InstrumentHandler(self)
        self.track_handler = TrackHandler(self)

        self.dispatch: Dict[str, callable] = {}
        self._load_dispatch()

    def _load_dispatch(self):
        for handler in [
            self.info_handler,
            self.macro_handler,
            self.instrument_handler,
            self.track_handler
        ]:
            self.dispatch.update(collect_handlers(handler))       

    def execute(self, project, input_file) -> None:
        self.project = project
        self.current_pattern = 0

        # TODO better exception handling
        try:
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
                        continue
                    
                    print(first_word)
                    handle(project, line)
            
        except Exception as e:
            # for file not open error
            print("[E] {}".format(e))
            exit(1)
    
