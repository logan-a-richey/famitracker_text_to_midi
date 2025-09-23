// constants.h

#ifndef CONSTANTS_H
#define CONSTANTS_H 

enum struct InstrumentType { 
    INST_2A03, 
    INST_VRC6, 
    INST_VRC7, 
    INST_FDS, 
    INST_N163, 
    INST_S5B 
};

enum struct MacroType { 
    VOL, 
    ARP, 
    PIT, 
    HPI, 
    DUT 
}; 

#endif // CONSTANTS_H

