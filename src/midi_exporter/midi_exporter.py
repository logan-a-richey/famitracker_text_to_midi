# midi_exporter.py

import os 

from util.custom_logger import Logger
logger = Logger(__name__)

from helpers.helper_functions import clean_string, classify_token_type
from helpers.constants import TokenType, SUBDIVISION 

# from submodules.midi_writer_cpp.python_usage.midi_writer import MidiWriter
from midi_exporter.midi_writer import MidiWriter
from helpers.regex_patterns import RegexPatterns
    
class ColContext:
    ''' Contains buffered note data '''

    def __init__(self):
        self.is_playing = False
        self.start = 0          # 0 or greater
        self.pitch = 60         # middle c
        self.instrument = 0     # default inst
        self.velocity = 15      # default hex max

NOTE_OFFSETS = { 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11 }
def get_token_pitch(token: str, note_type: int) -> int:
    if note_type == TokenType.NOTE_ON:
        pitch = NOTE_OFFSETS.get(token[0], 0)

        accidental = token[1]
        if accidental == '#':
            pitch += 1
        elif accidental == 'b':
            pitch -= 1

        octave = int(token[2])
        pitch += octave * 12
        return pitch
    elif note_type == TokenType.NOISE_ON:
        pitch = int(token[0], 16)
        return pitch
    else:
        raise ValueError("Could not convert token to Midi pitch: {}".format(token))

def get_token_inst(token: str, context: ColContext) -> int:
    try: 
        return int(token.split()[1], 16)
    except:
        return context.instrument

def get_token_vol(token: str, context: ColContext) -> int:
    try: 
        return int(token.split()[2], 16) * 8
    except:
        return context.velocity

class MidiExporter:
    def __init__(self):
        self.col_contexts = []
        self.midi = MidiWriter()

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
    
    def add_note_if_valid(self, 
        track: int, 
        channel: int, 
        start: int, 
        duration: int,
        pitch: int, 
        velocity: int
    ) -> None:
        if duration <= 0:
            print("Could not add note: Zero or negative duration.")
            return
        if velocity <= 0:
            print("Could not add note: Zero or negative velocity.")
            return

        self.midi.add_note(track, channel, start, duration, pitch, velocity) 
    
    def _handle_note(self, token: str, i: int, j: int) -> None:
        '''
        Handle note event and midi writing for a token.

        @param token: Famitracker substring in form "... .. . ..."
        @param i: row index
        @param j: col index
        '''

        context = self.col_contexts[j]
        note_type = classify_token_type(token)

        start = i * SUBDIVISION
        duration = start - context.start 
        inst = get_token_inst(token, context)
        vol = get_token_vol(token, context)
        if vol > 127 or vol < 0:
            raise ValueError("Vol OOB: {}".format(vol))
        
        if note_type in (TokenType.NOTE_ON, TokenType.NOISE_ON):
            if context.is_playing:
                self.add_note_if_valid(j, j % 2, context.start, duration, context.pitch, context.velocity)

            context.is_playing = True
            context.start = start
            context.pitch = get_token_pitch(token, note_type)
            context.instrument = inst
            context.velocity = vol

        elif note_type in (TokenType.NOTE_OFF, TokenType.NOTE_RELEASE) or vol == 0:
            if context.is_playing:
                self.add_note_if_valid(j, j % 2, context.start, duration, context.pitch, context.velocity)

            context.is_playing = False
        
    def export_track(self, project, track, project_path: str) -> None:
        # handle file io
        output_file_name = "track_{}_{}".format(track.index, track.name)
        output_file_name = clean_string(output_file_name) + ".mid"
        output_file_path = os.path.join(project_path, output_file_name)
        
        midi = MidiWriter()
        track_idx = midi.add_track()
        midi.set_channel(0, 1)  # channel 0, program 1 (e.g., piano)
        midi.add_bpm(track_idx, 0, 120)
        midi.add_time_signature(track_idx, 0, 4, 4)
        
        # TODO
        midi.add_bpm(0, 0, 120)

        self.col_contexts = [ColContext() for _ in range(track.num_cols)]
        
        # parse Track
        for i, line in enumerate(track.lines):
            tokens = [token.strip() for token in line.split("|")[1:] ]
            for j, token in enumerate(tokens):
                self._handle_note(token, i, j)
        
        midi.save(output_file_path)
        logger.info("Wrote file: {}".format(output_file_path)) 

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
