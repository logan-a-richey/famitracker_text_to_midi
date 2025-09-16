// macro.h

#pragma once 

#include <vector>

struct Macro {
    int type, index, loop, release, setting;
    std::vector<int> macro;
};