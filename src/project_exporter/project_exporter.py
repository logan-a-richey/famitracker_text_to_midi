# midi_exporter.py

import os 
import re
from typing import Optional

from util.custom_logger import Logger, LoggingLevels
logger = Logger(__name__)
logger.set_level(LoggingLevels.DEBUG)

from helpers.helper_functions import clean_string
from helpers.regex_patterns import RegexPatterns
from submodules.mock_midi_writer_py.midi_writer import MidiWriter

class ProjectExporter:
    def __init__(self):
        # store persistent state
        self.project: Optional["Project"] = None 
        self.track: Optional["Track"] = None
        self.midi: Optional["MidiWriter"] = None
        
        self.rows_per_beat: int = 4
        return 

    def _setup_midi_writer(self):
        self.midi = MidiWriter()
        self.midi.add_bpm(0, 0, 150)
        self.midi.add_time_signature(0, 0, 4, 4)

    def _handle_speed(self, line: str):
        ''' 
        Handle FXX and OXX (Groove) Events
        
        For FXX:
        if XX <= project.split, then set track.curr_speed to XX, set track.curr_tempo to track.tempo
        if XX > project.split, then set track.curr_speed to track.speed, and set track.curr_tempo to XX
        where XX is bounded 1 to 127

        For OXX
        XX represents the default groove. If XX is not in the Groove list, select the last groove.

        FXX and OXX switch modes from Speed to Groove mode. Speed mode is by default.
        '''
        
        speed_matches = RegexPatterns.EFFECT_SPEED_AND_TEMPO.findall(line)
        if not speed_matches:
            return 
        last_match = speed_matches[-1]
        match_type = last_match[0]
        match_value = int(last_match[1:], 16)

        if match_type == "F":
            return 
        
        elif match_type == "O":
            return 
        

        return 
            
    def _export_track(self, track: "Track", output_dir: str) -> None:
        self.track = track 

        self._setup_midi_writer()

        for i, line in enumerate(self.track.lines):
            self._handle_speed()

        # export midi
        output_filename = clean_string("TRACK_{}_{}".format(track.index, track.name)) + ".mid"
        output_path = os.join(output_dir, output_filename)
        
        logger.info("Created {}".format(output_path))
        self.midi.save(output_path)

        return 
    
    def export_project(self, project: "Project", output_dir: str, rows_per_beat: int) -> None:
        ''' Export all Tracks in a Project '''
        self.project = project 
        self.rows_per_beat = rows_per_beat 

        for track in project.tracks:
            self._export_track(track, output_dir) 
        
        return 
