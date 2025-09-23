// project_loader.h

#ifndef PROJECT_LOADER_H
#define PROJECT_LOADER_H 

#include <string>
#include <unordered_map>
#include <vector> 

struct Project;

class ProjectLoader {
private:
    int pattern_idx;
    int track_idx; 

private:

public:
    void load_project(Project p, std::string& input_file);
};

#endif // PROJECT_LOADER_H
