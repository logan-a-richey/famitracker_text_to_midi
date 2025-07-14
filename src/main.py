#!/usr/bin/env python3
# main.py
'''
TODO: 
Ideal usage:
./program.py --input <FILE> --destination <OUTPUT_PATH> --subdivision <INTEGER>

--- Additional Effects ---
Debug arpeggio effect   (00c)
Debug pitch bend effect (Rxx Qxx)
Note cut and delay      (Sxx, Gxx)
Substring or noise "smart" drum mapping

Fix incorrect MIDITRACK add_note()

Argparse CLI
WXPython Desktop APP
Web Upload and Download APP

Update README
'''

import os
import re
import sys
sys.dont_write_bytecode = True

from helpers.helper_functions import clean_string

from data.project import Project 
from project_loader.project_loader import ProjectLoader
from project_formatter.project_formatter import ProjectFormatter
from project_exporter.project_exporter import ProjectExporter

def get_input_file() -> str:
    ''' Get input file from cmdline '''

    try:
        input_file = sys.argv[1]
    except:
        print("[E] Usage: ./main <input.txt")
        exit(1)
    return input_file

#def get_output_path():
#    try:
#        output_path = sys.argv[2]        
#    except:
#        export_dir_name = "Exports"
#        output_path = os.path.join(os.getcwd(), export_dir_name)
#        os.makedirs(output_path, exist_ok=True)
#    return output_path
#
#def get_rows_per_beat() -> int:
#    try:
#        return int(sys.argv[3])
#    except:
#        return 4

def main():
    ''' Program entry point '''

    # get input file from the terminal
    input_file = get_input_file()
    rows_per_beat = 8

    #output_path = get_output_path()
    #rows_per_beat = get_rows_per_beat()

    # setup container and helper classes
    project = Project()
    project.rows_per_beat = rows_per_beat

    # parse and export
    stage1 = ProjectLoader()
    stage2 = ProjectFormatter()
    stage3 = ProjectExporter()

    # setup output dir path
    #project_output_dir_name = clean_string(project.name, pascal=True)
    #if not project_output_dir_name:
    midi_exports_dir = "Exports"

    project_dir_name = os.path.splitext(os.path.basename(input_file))[0]
    project_dir_name = clean_string(project_dir_name, pascal=True) # JayhawkerMarchBees

    relative_path = os.path.join(midi_exports_dir, project_dir_name)
    project_dir_path = os.path.abspath(relative_path)
    os.makedirs(project_dir_path, exist_ok=True)

    # run the program
    stage1.load_project(project, input_file)
    #project.show()
    stage2.format_project(project)
    stage3.export_project(project, project_dir_path, rows_per_beat)

if __name__ == "__main__":
    main()

