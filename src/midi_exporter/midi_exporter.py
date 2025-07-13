# midi_exporter.py

import os 

from util.custom_logger import Logger
logger = Logger(__name__)

from helpers.helper_functions import clean_string, get_midi_pitch, classify_token_type
from helpers.constants import TokenType, SUBDIVISION 

from submodules.midi_writer_cpp.python_usage.midi_writer import MidiWriter
from helpers.regex_patterns import RegexPatterns
    
class NoteEvent:
    def __init__(self):
        self.start = 0          # 0 or greater
        self.duration = 120     # non zero 
        self.pitch = 60         # middle c
        self.instrument = 0     # default inst
        self.velocity = 15      # default hex max
        self.is_playing = False

class MidiExporter:
    def __init__(self):
        self.note_events = []
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
 
    def note_on(self, col: int, start: int, pitch: int, inst: int, vol: int) -> None:
        ne = self.note_events[col]
        if ne.is_playing:
            dur = start - ne.duration
            vel = ne.velocity * 12
            self.midi.add_note(col, col % 2, ne.start, dur, ne.pitch, vel)
        
        ne.is_playing = True
        ne.start = start
        ne.pitch = pitch 
        ne.inst = inst 
        ne.velocity = vol

    def note_off(self, col: int, start: int):
        ne = self.note_events[col]
        if ne.is_playing:
            dur = start - ne.duration
            vel = ne.velocity * 12
            self.midi.add_note(col, col % 2, ne.start, dur, ne.pitch, vel)
        
        ne.is_playing = False

    def export_track(self, project, track, project_path: str) -> None:
        # handle file io
        output_file_name = "track_{}_{}".format(track.index, track.name)
        output_file_name = clean_string(output_file_name) + ".mid"
        output_file_path = os.path.join(project_path, output_file_name)
        
        self.midi = MidiWriter()
        
        # TODO
        self.midi.add_bpm(0, 0, 120)

        self.note_events = [NoteEvent() for _ in range(track.num_cols)]
        
        # parse Track
        for i, line in enumerate(track.lines):
            tokens = [token.strip() for token in line.split("|")[1:] ]
            for j, token in enumerate(tokens):
                note_event = classify_token_type(token)
                start = i * SUBDIVISION 

                if note_event == TokenType.NOTE_ON:
                    pitch = get_midi_pitch(token)
                    inst = 0 # TODO
                    vol = 15
                    self.note_on(j, start, pitch, inst, vol)

                elif note_event in [TokenType.NOTE_OFF, TokenType.NOTE_RELEASE]:
                    self.note_off(j, start)

        self.midi.save(output_file_path)

    
    def export_project(self, project, output_dir_path: str):
        ''' Export all Tracks in Project as MIDI '''

        self.test_export(output_dir_path)

        # create a folder for this project 
        cleaned_project_name = clean_string(project.title, mode="Pascal")
        if not cleaned_project_name:
            cleaned_project_name = "DefaultProject"

        project_path = os.path.join(output_dir_path, cleaned_project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # export tracks
        for track in project.tracks:
            self.export_track(project, track, project_path)
