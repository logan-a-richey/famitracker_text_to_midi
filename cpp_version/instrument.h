// instrument.h 

#pragma once 

#include "macro.h"

#include <vector>
#include <array>
#include <unordered_map>
#include <string> 

struct KeyDpcm { 
    int inst, octave, note, sample, pitch, loop, loop_point, delta;
};

struct Instrument {
    Instrument() : 
        index(0),
        seq_vol(-1), seq_arp(-1), seq_pit(-1), seq_hpi(-1), seq_dut(-1),
        name("default instrument"),
        macro_vol(nullptr), macro_arp(nullptr), macro_pit(nullptr), macro_hpi(nullptr), macro_dut(nullptr) {}

    int index;
    int seq_vol, seq_arp, seq_pit, seq_hpi, seq_dut;
    std::string name;
    
    Macro* macro_vol;
    Macro* macro_arp; 
    Macro* macro_pit; 
    Macro* macro_hpi; 
    Macro* macro_dut;
    
    std::unordered_map<int, KeyDpcm> key_dpcm;
};

struct InstVRC7 : Instrument {
    InstVRC7() : patch(0) {
        registers.fill(0);
    }

    int patch;
    std::array<int, 8> registers; 
};

struct InstN163 : Instrument {
    InstN163() : w_size(0), w_pos(0), w_count(0) {}

    int w_size, w_pos, w_count;
    std::unordered_map<int, std::vector<int>> waves;
};

struct InstFDS : Instrument {
    std::vector<int> fds_wave;
    std::vector<int> fds_mod;
};

