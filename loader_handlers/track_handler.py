# track_handler.py

import re
from helpers.regex_patterns import RegexPatterns
from loader_handlers.handler_registry import register
from data.track import Track

class TrackHandler:
    def __init__(self, project_loader):
        self.project_loader = project_loader 

    @register("TRACK")
    def handle_track(self, project, line):
        pass
    
    @register("COLUMNS")
    def handle_columns(self, project, line):
        pass
    
    @register("ORDER")
    def handle_order(self, project, line):
        pass
    
    @register("PATTERN")
    def handle_pattern(self, project, line):
        pass
    
    @register("ROW")
    def handle_row(self, project, line):
        pass

#   def handle_track(self, line: str) -> None:
#       # TODO regex
#       # TODO load data
#
#       new_track = Track()
#       self.project.tracks.append(new_track)
#       pass
#   
#   def handle_columns(self, line: str) -> None:
#       if not self.project.tracks:
#           raise ValueError("Track not initialized")
#       current_track = self.projet.tracks[-1]
        # TODO regex
        # TODO load data
#       pass

#   def handle_order(self, line: str) -> None:
#       if not self.project.tracks:
#           raise ValueError("Track not initialized")
#       current_track = self.projet.tracks[-1]
#       # TODO regex
#       # TODO load data
#       pass

#   def handle_pattern(self, line: str) -> None:
#       if not self.project.tracks:
#           raise ValueError("Track not initialized")
#       current_track = self.projet.tracks[-1]
#       # TODO regex
#       # TODO load data
#       pass

#   def handle_row(self, line: str) -> None:
#       if not self.project.tracks:
#           raise ValueError("Track not initialized")
#       current_track = self.projet.tracks[-1]
#       # TODO regex
#       # TODO load data
#       pass

