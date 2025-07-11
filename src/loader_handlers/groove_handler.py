# groove_handler.py

from loader_handlers.handler_registry import register 
from helpers.regex_patterns import RegexPatterns
from data.groove import Groove

class GrooveHandler:
    def __init__(self):
        pass

    @register("GROOVE")
    def handle_groove(self, project, line):
        regex_match = RegexPatterns.GROOVE.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")

        index, size = list(map(int, regex_match.group("index", "size")))
        data = list(map(line.split(":")[1].strip().split()))

        groove_obj = Groove(index, size, data)
        project.grooves[index] = groove_obj

    @register("USEGROOVE")
    def handle_use_groove(self, project, line):
        lst = list(map(int, line.split(":")[1].strip().split()))
        project.usegroove = lst