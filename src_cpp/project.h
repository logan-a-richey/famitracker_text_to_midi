// project.h 

#ifndef PROJECT_H 
#define PROJECT_H

#include <string>
#include <unordered_map>
#include <vector>

#include "macro.h"
#include "instrument.h"
#include "track.h"

struct Project {
    std::string  title, author, copyright, comment;
    int machine, framerate, expansion, vibrato, split, n163channels;
    std::unordered_map<std::string, Macro> macros;
    std::unordered_map<int, Instrument> instruments;
    std::vector<Track> tracks;
}; 

#endif // PROJECT_H

