// project_scanner.h

#pragma once 

#include <string>

#include "project.h"

class ProjectScanner {
private:
    bool is_blank(const std::string& s);
    std::string convert_line_to_ascii(const std::string& line);
    
    // line handlers
    void handle_song_info(Project& project, const std::string& line);
    void handle_comment(Project& project, const std::string& line);
    void handle_global_setting(Project& project, const std::string& line);
    void handle_macro(Project& project, const std::string& line);
    
    void handle_inst2a03(Project& project, const std::string& line);
    void handle_instvrc6(Project& project, const std::string& line);
    void handle_instvrc7(Project& project, const std::string& line);
    void handle_instfds(Project& project, const std::string& line);
    void handle_instn163(Project& project, const std::string& line);
    void handle_insts5b(Project& project, const std::string& line);
    
    void handle_fdswave(Project& project, const std::string& line);
    void handle_fdsmod(Project& project, const std::string& line);
    void handle_fdsmacro(Project& project, const std::string& line);
    void handle_n163wave(Project& project, const std::string& line);
    
    void handle_track(Project& project, const std::string& line);
    void handle_columns(Project& project, const std::string& line);
    void handle_order(Project& project, const std::string& line);
    void handle_pattern(Project& project, const std::string& line);
    void handle_row(Project& project, const std::string& line);

public:
    void scan_project(Project& project, const std::string file_path);
};


