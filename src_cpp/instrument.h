// instrument.h 

#pragma once 

#include <vector>
#include <unordered_map>
#include <string> 

struct Instrument {
    int index;
    std::string name;
    Macro* macro_vol, macro_arp, macro_pit, macro_hpi, macro_dut;
};

struct InstVRC7 : Instrument {

};

struct InstN163 : Instrument {

};

struct InstFDS : Instrument {

};