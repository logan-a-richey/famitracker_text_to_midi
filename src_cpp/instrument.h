// instrument.h

#ifndef INSTRUMENT_H
#define INSTRUMENT_H 

#include <string>

class Instrument {
public:
    int index;
    int seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut;
    std::string name;
    
    // loaded macros;
    Macro* macro_vol;
    Macro* macro_arp;
    Macro* macro_pit;
    Macro* macro_hpi;
    Macro* macro_dut;
};

class InstVRC7 : public Instrument {
public:
    int patch;
    std::vector<int> registers;
};

class InstFDS : public Instrument {
public:
    bool mod_enable;
    int mod_depth;
    int mod_speed;
    std::vector<int> fds_wave;
    std::vector<int> fds_mod;
};

class InstN163 : public Instrument {
public:
    int w_size, w_pos, w_count;
    std::unordered_map<int, std::vector<int>> waves;
};

#endif // INSTRUMENT_H
