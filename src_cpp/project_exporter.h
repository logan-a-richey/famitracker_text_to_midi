// project_exporter.h 

#ifndef PROJECT_EXPORTER_H
#define PROJECT_EXPORTER_H 

#include <string>

struct Project;

class ProjectExporter {
public:
    void export_project(Project p, std::string& output_path);
};

#endif // PROJECT_EXPORTER_H 
