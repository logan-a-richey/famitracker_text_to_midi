// macro.h

#ifndef MACRO_H
#define MACRO_H 

#include <vector>

#include "constants.h"

struct Macro {
    InstrumentType i_type;
    MacroType m_type;
    int loop, release, setting;
    std::vector<int> sequence; 
};

#endif // MACRO_H

