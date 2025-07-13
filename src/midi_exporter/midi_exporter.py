# midi_exporter.py

import os 

from util.custom_logger import Logger
logger = Logger(__name__)

from helpers.helper_functions import clean_string 
from submodules.midi_writer_cpp.python_usage.midi_writer import MidiWriter

class MidiExporter:
    def __init__(self):
        pass

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
        DEFAULT_VELOCITY = 0
        QUARTER_NOTE = 480
        notes = [60, 62, 64, 65, 67, 69, 71, 72]
        for tick, note in enumerate(notes):
            midi_writer.add_note(DEFAULT_TRACK, DEFAULT_CHANNEL, QUARTER_NOTE * tick, QUARTER_NOTE, note, DEFAULT_VELOCITY)

        # export finished
        midi_writer.save(output_filepath)
        logger.info("File created: {}".format(output_filepath))
        return 
    
    def export_project(self, project, output_dir_path: str):
        ''' Export all Tracks in Project as MIDI '''

        cleaned_project_name = clean_string(project.title, mode="Pascal")
        if not cleaned_project_name:
            cleaned_project_name = "MiscProject"

        project_path = os.path.join(output_dir_path, cleaned_project_name)
        os.makedirs(project_path, exist_ok=True)

        for track in project.tracks:
            # setup filename and filepath
            unclean_string = "track_{}_{}".format(track.index, track.name)
            output_filename = clean_string(unclean_string) + ".mid"
            output_filepath = os.path.join(project_path, output_filename)
        
        # TODO 
                 
        return
                
