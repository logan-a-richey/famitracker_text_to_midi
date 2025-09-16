# midi_exporter.py

import os 
import re
from typing import Optional, List

from util.custom_logger import Logger, LoggingLevels
logger = Logger(__name__)
logger.set_level(LoggingLevels.VERBOSE)

from helpers.helper_functions import clean_string, classify_token_type
from helpers.fami_helpers import FamiHelpers 
from helpers.regex_patterns import RegexPatterns
from helpers.constants import TokenType

from submodules.mock_midi_writer_py.midi_writer import MidiWriter
from data.col_context import ColContext

class ProjectExporter:
    def __init__(self):
        # store persistent state
        self.project: Optional["Project"] = None 
        self.track: Optional["Track"] = None
        self.midi: Optional["MidiWriter"] = MidiWriter()
        
        self.rows_per_beat: int = 4
        self.SUBDIVISION = 120 
        self.set_subdivision(4)

        self.contexts: List["ColContext"] = []

    def set_subdivision(self, ticks_per_row: int):
        ''' 
        Quarter = 480 ticks. 
        We can shrink the subdivision using a Ticks Per Row scheme.
        
        ticks_per_row = 4 ; 16th note
        ticks_per_row = 8 ; 32nd note
        ticks_per_row = 16 ; 64nd note
        
        ticks_per_row = 3 ; 12th note (eighth note triplet)
        ticks_per_row = 6 ; 24th note (16th note triplet)
        '''

        self.SUBDIVISION = int(480 / ticks_per_row )
        return 

    def _setup_midi_writer(self):
        ''' Sets up MIDI state '''

        self.midi = MidiWriter()
        # TODO get initial Track BPM
        self.midi.add_bpm(0, 0, 150)
        self.midi.add_time_signature(0, 0, 4, 4)
        return 
    
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
            if match_value <= self.project.split:
                self.track.curr_speed = match_value 
                self.track.curr_tempo = self.track.tempo
            else: 
                self.track.curr_speed = self.track.speed 
                self.track.curr_tempo = match_value 
            logger.info("{} | Speed changed = {} | Tempo changed = {}".format(last_match, self.track.curr_speed, self.track.curr_tempo))
            return 
        
        elif match_type == "O":
            if len(self.project.grooves) == 0:
                return

            groove_average_speed = 1 
            if match_value in self.project.grooves:
                groove_obj = self.project_grooves[match_value]
                groove_average_speed = sum(groove_obj.data) / len(groove_obj.data)
            else:
                groove_obj = self.project.grooves[-1]
                groove_average_speed = sum(groove_obj.data) / len(groove_obj.data)

            self.track.curr_speed = groove_average_speed
            logger.info("Groove speed changed: {}".format(groove_average_speed))            
            return 

        return 

    def _sync_context(self, context: "ColContext"):
        ''' 
        ColContext contains two NoteData objects
        context.curr contains the current data 
        context.last contains the cached data
        '''

        context.last.start = context.curr.start
        context.last.pitch = context.curr.pitch
        context.last.instrument = context.curr.instrument 
        context.last.volume = context.curr.volume

        context.last.arp_x = context.curr.arp_x
        context.last.arp_y = context.curr.arp_y 
        return 
     
    def _handle_pitch(self, context: "ColContext", token: str):
        ''' Handle XXX .. . ...'''

        token_part = token.split()[0]
        
        note_on_match = RegexPatterns.TOKEN_NOTE_ON.match(token_part) 
        noise_on_match = RegexPatterns.TOKEN_NOISE_ON.match(token_part)
        if note_on_match:
            pitch = FamiHelpers.get_note_on_pitch(token_part)
        elif noise_on_match:
            pitch = FamiHelpers.get_noise_on_pitch(token_part)
        else:
            return
        
        context.curr.pitch = pitch
        return 
    
    def _handle_instrument(self, context: "ColContext", token: str):
        ''' Handle ... XX . ...'''
        
        token_part = token.split()[1]
        regex_match = RegexPatterns.TOKEN_INST.match(token_part)
        if not regex_match:
            return 
        
        value = int(regex_match.group(0), 16)
        context.curr.instrument = value
        return 
    
    def _handle_volume(self, context: "ColContext", token: str):
        ''' Handle ... .. X ...'''
        
        token_part = token.split()[2]
        regex_match = RegexPatterns.TOKEN_VOL.match(token_part)
        if not regex_match:
            return 
        
        value = int(regex_match.group(0), 16)
        context.curr.volume = value
        return 

    def add_note_if_valid(self, context: "ColContext"):
        ''' Add a MIDI note if it is cached in ColContext.last object '''

        if not context.is_playing:
            return 
        
        # ensure that a context can only add a note once per loop iteration
        if not context.one_shot:
            return 
        context.one_shot = False 

        duration = context.curr.start - context.last.start
        if duration == 0:
            logger.warn("Zero duration note. {}".format(context))
            return 

        scaled_volume = context.last.volume * 8 

        self.midi.add_note(
            context.idx + 1, # track index
            context.idx % 2, # alternate piano channels
            context.last.start,
            duration, 
            context.last.pitch,
            scaled_volume
        )

        # NOTE Add 00C arpeggio notes
        if context.last.arp_x:
            self.midi.add_note(
                context.idx + 1, # track index
                context.idx % 2, # alternate piano channels
                context.last.start,
                duration, 
                context.last.pitch + context.last.arp_x,
                scaled_volume
            )
        if context.last.arp_y and (context.last.arp_y != context.last.arp_x):
            self.midi.add_note(
                context.idx + 1, # track index
                context.idx % 2, # alternate piano channels
                context.last.start,
                duration, 
                context.last.pitch + context.last.arp_y,
                scaled_volume
            )
        
        # TODO add drum note if valid

        return
    
    def _handle_pitch_bend(self, context: "ColContext", token: str) -> bool:
        ''' 
        Handles pitch bend. Qxx = upward bend, Rxx = downward bend.

        If: token contains NOTE_ON or NOISE_ON, just apply pitch shift to context.curr.pitch
        Else: treat it like a note trigger.
        '''

        if not context.is_playing:
            return 

        pitch_bend_matches = RegexPatterns.EFFECT_RQ.findall(token)
        if not pitch_bend_matches:
            return 
        
        token_type = classify_token_type(token)
        
        # Case 1:
        if token_type not in [TokenType.NOTE_ON, TokenType.NOISE_ON]:
            self.add_note_if_valid(context)
        
        # Apply pitch shift:
        last_match = pitch_bend_matches[-1]
        value = int(last_match[2], 16)
        
        if last_match[0] == "Q":
            context.curr.pitch += value
        if last_match[0] == "R":
            context.curr.pitch -= value 
        
        # Case 1 (continued): If this is a standalone pitch bend, sync to start a new note:
        if token_type not in [TokenType.NOTE_ON, TokenType.NOISE_ON]:
            context.is_playing = True
            self._sync_context(context)
        
        return 
    
    def _handle_arpeggio(self, context: "ColContext", token: str):
        ''' 0XY represents an arpeggio, where X and Y are integer offsets from the current pitch. '''

        arp_matches = RegexPatterns.EFFECT_ARP.findall(token)
        if not arp_matches:
            return 
        
        last_match = arp_matches[-1]
        x = int(last_match[1], 16)
        y = int(last_match[2], 16)
        context.curr.arp_x = x 
        context.curr.arp_y = y
        
        return 

    def _export_track(self, track: "Track", output_dir: str) -> None:
        ''' 
        Exports a FamiTracker Track into MIDI 
        Handles note durations, volumes, and notable FamiTracker effects
        '''

        # setup
        self.track = track 
        self.contexts = [ColContext(i) for i in range(self.track.num_cols)]

        self._setup_midi_writer()

        # NOTE read and loop through Track lines:
        for i, line in enumerate(self.track.lines):
            # DEBUG
            logger.verbose("LINE_NO {} | {}".format(i, line))
            
            # TODO handle MIDI BPM changes
            self._handle_speed(line)

            tokens = [token.strip() for token in line.split("|")[1:]]
            for j, token in enumerate(tokens):
                midi_tick = i * self.SUBDIVISION 
                token_type = classify_token_type(token)
                
                # NOTE context setup
                context = self.contexts[j]
                context.one_shot = True
                context.curr.start = midi_tick

                # NOTE - handle effects
                self._handle_pitch(context, token) 
                self._handle_instrument(context, token)
                self._handle_volume(context, token)

                self._handle_pitch_bend(context, token)
                self._handle_arpeggio(context, token)

                # NOTE add and release notes
                # store new notes
                if (token_type == TokenType.NOTE_ON) or (token_type == TokenType.NOISE_ON):
                    self.add_note_if_valid(context)
                    context.is_playing = True    
                    self._sync_context(context)
                # note off events
                elif (token_type == TokenType.NOTE_OFF) or (token_type == TokenType.NOTE_RELEASE) or (context.curr.volume == 0):
                    self.add_note_if_valid(context)
                    context.is_playing = False    
                    self._sync_context(context)
                                
        # NOTE export midi
        output_filename = clean_string("TRACK_{}_{}".format(track.index, track.name)) + ".mid"
        output_path = os.path.join(output_dir, output_filename)
        
        logger.info("Created {}".format(output_path))
        self.midi.save(output_path)

        return 
    
    def export_project(self, project: "Project", output_dir: str, rows_per_beat: int) -> None:
        ''' Export all Tracks in a Project '''
        
        self.project = project 
        self.rows_per_beat = rows_per_beat 
        self.set_subdivision(rows_per_beat)

        for track in project.tracks:
            self._export_track(track, output_dir) 
        
        return 

