#!/usr/bin/env python3
# main.py

import os
import re
import sys
sys.dont_write_bytecode = True


from data.project import Project 
from loader_handlers.project_loader import ProjectLoader
from formatter_handlers.project_formatter import ProjectFormatter
from midi_exporter.midi_exporter import MidiExporter

def get_input_file() -> str:
    ''' Get input file from cmdline '''

    try:
        input_file = sys.argv[1]
    except:
        print("[E] Usage: ./main <input.txt")
        exit(1)
    return input_file

def get_output_path():
    try:
        output_path = sys.argv[2]        
    except:
        export_dir_name = "MidiExports"
        output_path = os.path.join(os.getcwd(), export_dir_name)
        os.makedirs(output_path, exist_ok=True)
    return output_path

def get_rows_per_beat() -> int:
    try:
        return int(sys.argv[3])
    except:
        return 4

def main():
    ''' Program entry point '''

    # get input file from the terminal
    input_file = get_input_file()
    output_path = get_output_path()
    rows_per_beat = get_rows_per_beat()

    # setup container and helper classes
    project = Project()
    project.rows_per_beat = rows_per_beat

    # parse and export
    stage1 = ProjectLoader()
    stage2 = ProjectFormatter()
    stage3 = MidiExporter()

    # setup output dir path
    output_dir_path = os.path.join( os.getcwd(), output_path)        

    # run the program
    stage1.load_project(project, input_file)
    #project.show()
    stage2.format_project(project)
    stage3.export_project(project, output_dir_path, rows_per_beat)

if __name__ == "__main__":
    main()
