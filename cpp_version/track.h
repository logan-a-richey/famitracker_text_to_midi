// track.h

#pragma once 

#include <string>
#include <unordered_map>
#include <vector>

struct Track {
    int num_rows, num_cols, tempo, speed;
    std::string name;

    std::vector<int> eff_cols;

    std::unordered_map<std::string, std::vector<int>> orders;
    std::unordered_map<std::string, std::string> tokens;
};
