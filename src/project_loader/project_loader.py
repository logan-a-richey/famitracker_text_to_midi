# project_loader.py

from util.custom_logger import Logger
logger = Logger(__name__)

import re
from typing import Optional, Dict, List, Callable 

from data.macro import Macro 
from data.instrument import Inst2A03, InstVRC6, InstVRC7, InstFDS, InstN163, InstS5B
from data.track import Track

from project_loader.info_handler import InfoHandler
from project_loader.macro_handler import MacroHandler
from project_loader.instrument_handler import InstrumentHandler
from project_loader.track_handler import TrackHandler
from project_loader.dpcm_handler import DPCMHandler
from project_loader.groove_handler import GrooveHandler
from project_loader.special_handler import SpecialHandler

from project_loader.handler_registry import collect_handlers

class ProjectLoader:
    ''' 
    Main helper class to parse lines from a FamiTracker text export file.
    Contains several helper classes that each contain additional line handler methods.
    Each line handler adds information to Project class.

    New methods can be added to the dispatch table using thje @register("TAG_NAME") decorator.
    
    NOTE: Be sure that every function and TAG_NAME is unique.
    Otherwise, Python will overwrite the function and that method will not be added to the dispatch.
    '''

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
        """Main method to call"""

        try:
            with open(input_file, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    first_word = line.split()[0]
                    handle = self.dispatch.get(first_word)

                    if not handle:
                        logger.warn("Line {}: Unhandled line: {}".format(line_num, line))
                        continue

                    try:
                        handle(project, line)
                    except Exception as e:
                        logger.warn("Handler error: {} | Line {}: ".format(e, line))

        except FileNotFoundError:
            logger.error("File not found: {}".format(input_file))
        except PermissionError:
            logger.error("Permission denied: {}".format(input_file))
        except OSError as e:
            logger.error("OS error while opening file '{}': {}".format(input_file, e))
        except Exception as e:
            logger.error("Something unexpected has happened: {}".format(e))
