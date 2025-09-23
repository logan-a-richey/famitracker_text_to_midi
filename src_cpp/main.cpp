// main.cpp

#include <iostream>
#include <string>

#include "project.h"
#include "project_loader.h"
#include "project_formatter.h"
#include "project_exporter.h"

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "[ERROR] Usage: ./main <input> <output path>" << std::endl;
        exit(1);
    }
    
    std::string input_file = argv[1];
    std::string output_path = argv[2];

    std::cout << "[INFO] Input file  : " << input_file << std::endl;
    std::cout << "[INFO] Output path : " << output_path << std::endl;
    
    Project p;
    ProjectLoader pl;
    ProjectFormatter pf;
    ProjectExporter pe;

    pl.load_project(p, input_file);
    pf.format_project(p);
    pe.export_project(p, output_path);

    return 0;
}
