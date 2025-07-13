# midi_exporter.py

import os 

from util.custom_logger import Logger, LoggingLevels
logger = Logger(__name__)
logger.set_level(LoggingLevels.VERBOSE)

from helpers.helper_functions import clean_string, classify_token_type
from helpers.constants import TokenType, SUBDIVISION 

# CPP VERSION
# from submodules.midi_writer_cpp.python_usage.midi_writer import MidiWriter

# PYTHON VERSION
from midi_exporter.midi_writer import MidiWriter
from helpers.fami_helpers import FamiHelpers
from helpers.regex_patterns import RegexPatterns
from data.col_context import ColContext

class MidiExporter:
    def __init__(self):
        self.col_contexts = []
        self.midi = MidiWriter()
        self.fami_helpers = FamiHelpers()

    def test_export(self, output_dir_path: str):
        project_path = os.path.join(output_dir_path, "Test")
        os.makedirs(project_path, exist_ok=True)
        output_filename = "c_major_scale.mid"
        output_filepath = os.path.join(project_path, output_filename)
        
        # start the export
        logger.debug("Started file export: {}".format(output_filename))
        
        midi_writer = MidiWriter()
        midi_writer.add_time_signature(0, 0, 4, 4)
        midi_writer.add_bpm(0, 0, 133)

        DEFAULT_TRACK = 0
        DEFAULT_CHANNEL = 0
        DEFAULT_VELOCITY = 120
        QUARTER_NOTE = 480
        notes = [60, 62, 64, 65, 67, 69, 71, 72]
        for tick, note in enumerate(notes):
            midi_writer.add_note(DEFAULT_TRACK, DEFAULT_CHANNEL, tick * QUARTER_NOTE, QUARTER_NOTE, note, DEFAULT_VELOCITY)
            # midi_writer.add_note(0, 0, tick * 480, 480, note, 120)
        
        # export finished
        midi_writer.save(output_filepath)
        logger.info("File created: {}".format(output_filepath))
        return 

    def add_note_if_valid(self, context: "ColContext") -> None:
        if not context.is_playing:
            return 
        
        duration = context.curr_tick - context.last_tick
        if duration <= 0 :
            logger.warn("Duration OOB: {}".format(duration))
            return 
        if context.last_vol <= 0 or context.last_vol > 127:
            logger.warn("Velocity OOB: {}".format(context.last_vol))
            return 
        if context.pitch < 0 or context.pitch > 127:
            logger.warn("Pitch OOB: {}".format(context.pitch))
            return

        midi_args = [
            context.idx + 1, # track_idx
            context.idx  % 2 , # channel (alternate piano instruments)
            context.last_tick, # start 
            duration, 
            context.pitch, 
            context.last_vol
        ]
        logger.verbose("Added note: track={}, channel={}, start={}, duration={}, pitch={}, velocity={}".format(*midi_args)) 
        self.midi.add_note(*midi_args)
        return

    def export_track(self, project, track, path: str):
        self.midi = MidiWriter()

        self.midi.add_track()
        self.midi.add_track_name(0, clean_string(track.name), 0)
        self.midi.set_channel(0, 0)
        bpm = FamiHelpers.get_fami_bpm(track)
        self.midi.add_bpm(0, 0, bpm)
        self.midi.add_time_signature(0, 0, 4, 4)

        self.col_contexts = [ColContext(idx) for idx in range(track.num_cols)]

        for i, line in enumerate(track.lines):
            midi_tick = i * SUBDIVISION 

            tokens = [token.strip() for token in line.split("|")[1:]]
            for j, token in enumerate(tokens):
                context = self.col_contexts[j] 

                context.curr_vol = FamiHelpers.get_token_vol(token, context)
                context.curr_inst = FamiHelpers.get_token_inst(token, context)
                context.curr_tick = midi_tick 

                token_type = classify_token_type(token)
                if token_type == TokenType.NOTE_ON:
                    self.add_note_if_valid(context)

                    # prepare new note
                    context.is_playing = True 
                    context.last_tick = context.curr_tick
                    context.pitch = FamiHelpers.get_note_on_pitch(token)
                    context.last_inst = context.curr_inst 
                    context.last_vol = context.curr_vol

                elif token_type == TokenType.NOTE_OFF:
                    self.add_note_if_valid(context)
                    context.is_playing = False 
                #elif token_type == TokenType.NOISE_ON:
                #    self.add_note_if_valid(context)
                #    context.is_playing = True 
                else:
                    continue 
        
        name = clean_string(track.name)
        if not name:
            name = "new_song"
        filename = "track_{}_{}.mid".format(track.index, name)
        filepath = os.path.join(path, filename)
        self.midi.save(filepath)
        return
     
    def export_project(self, project, output_dir_path: str):
        ''' Export all Tracks in Project as MIDI '''

        # self.test_export(output_dir_path)

        # create a folder for this project 
        cleaned_project_name = clean_string(project.title, mode="Pascal")
        if not cleaned_project_name:
            cleaned_project_name = "DefaultProject"

        project_path = os.path.join(output_dir_path, cleaned_project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # export tracks
        for track in project.tracks:
            self.export_track(project, track, project_path)
