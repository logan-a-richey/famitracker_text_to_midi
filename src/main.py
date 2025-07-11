#!/usr/bin/env python3
# main.py

import sys
sys.dont_write_bytecode = True

from data.project import Project 
from loader_handlers.project_loader import ProjectLoader
from formatter_handlers.project_formatter import ProjectFormatter
# from project_exporter import ProjectExporter

def get_input_file() -> str:
    try:
        input_file = sys.argv[1]
    except:
        print("[E] Usage: ./main <input.txt")
        exit(1)
    return input_file

def main():
    input_file = get_input_file()

    project = Project()
    stage1 = ProjectLoader()
    stage2 = ProjectFormatter()
    #stage3 = ProjectExporter()

    stage1.load_project(project, input_file)
    stage2.format_project(project)

    #project.show()
    #for key, val in project.instruments.items():
    #    print("Index: {} | {}".format(key, val))

    # stage2.execute(project)
    
    # stage3.execute(project, output_path)
    
    return

if __name__ == "__main__":
    main()
