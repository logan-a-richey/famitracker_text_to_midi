// track.h

#ifndef TRACK_H
#define TRACK_H 

#include <vector>
#include <unordered_map>
#include <string>

struct Track {
    std::string name;
    int idx, num_rows, num_cols, tempo, speed;
    std::vector<int> eff_cols;
    std::unordered_map<int, std::vector<int>> orders; 
    std::unordered_map<std::string, std::string> tokens;
    std::vector<std::string> lines;
};

#endif // TRACK_H 
