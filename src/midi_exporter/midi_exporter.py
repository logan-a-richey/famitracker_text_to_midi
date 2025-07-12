# midi_exporter.py

import os 
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

from helpers.helper_functions import clean_string 
from submodules.midi_writer_cpp.python_usage.midi_writer import MidiWriter

class MidiExporter:
    def __init__(self):
        pass

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
            
            # start the export
            logger.debug("Started file export: {}".format(output_filename))
            
            midi_writer = MidiWriter()
            midi_writer.add_time_signature(0, 0, 4, 4)
            midi_writer.add_bpm(0, 0, 133)

            QUARTER_NOTE = 480
            for i in range(8):
                midi_writer.add_note(0, 0, QUARTER_NOTE * i, QUARTER_NOTE, 60 + i, 120)

            # export finished
            midi_writer.save(output_filepath)
            logger.info("File created: {}".format(output_filepath))
