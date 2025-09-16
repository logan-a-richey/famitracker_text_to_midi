// main.cpp

#include <iostream>
#include <string>
#include <unordered_map>
#include <vector> 
#include <regex>

#include "project.h"
#include "project_scanner.h"

// usage:
// ./main <input_file.txt>

int main(int argc, char** argv) 
{
    std::cout << "Running famitracker text-to-midi converter ..." << std::endl;

    std::string input_filename, output_filename; 

    // get input_filename
    if (argc >= 2) {
        input_filename = std::string(argv[1]);
    } else {
        std::cerr << "Usage: ./main <input.txt>" << std::endl;
        return 1;
    }

    // (optional) get output_filename
    if (argc >= 3) {
        output_filename = std::string(argv[2]);
    } else  {
        output_filename = "output.mid";
    }

    Project my_project; 
    ProjectScanner scanner;

    scanner.scan_project(my_project, input_filename);
    my_project.say();

    //format_project(my_project);
    //export_midi(my_project, output_filename);

    return 0;
}
