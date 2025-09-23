// project.h 

#pragma once 

#include "macro.h"
#include "instrument.h"
#include "track.h"

#include <string>
#include <unordered_map>
#include <vector>

class Project {
public:
    Project() : 
        title("default title"),
        author("default author"), 
        copyright("default copyright"),
        comment(""),
        machine(0),
        framerate(0),
        expansion(0),
        vibrato(1),
        split(32),
        n163channels(0) {}
    
    void say();

public:
    std::string title, author, copyright, comment;

    int machine, framerate, expansion, vibrato, split, n163channels;
    
    std::unordered_map<std::string, Macro> macros;
    
    std::unordered_map<int, Instrument> instruments;

    std::vector<Track> tracks;
};

