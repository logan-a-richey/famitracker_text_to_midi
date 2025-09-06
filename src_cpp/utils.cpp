// utils.cpp

#include "utils.h"

#include <iostream>
#include <string>
#include <fstream>
#include <regex> 
#include <unordered_map>
#include <sstream>

static std::string convert_line_to_ascii(std::string line) {
    std::string new_line;
    for (char c : line) {

    }

    return new_line;
}

static void handle_song_info(Project& project, const std::string& line) {
    std::cout << "in handle_song_info...\n";

    static std::regex pattern("^(TITLE|AUTHOR|COPYRIGHT)\\s+\"(.*)\".*$"); 
    std::smatch matches; 

    if (std::regex_search(line, matches, pattern)) {
        std::string key = matches[1];
        std::string value = matches[2];

        if (key == "TITLE") { project.title = value; }
        else if (key == "AUTHOR") { project.author = value; }
        else if (key == "COPYRIGHT") { project.copyright = value; }
    } else {
        std::cerr << "Regex failed: " << line << std::endl;
    }
}

static void handle_comment(Project& project, const std::string& line) {
    std::cout << "in handle_comment...\n";
    
    static std::regex pattern("^(COMMENT)\\s+\"(.*)\".*$"); 
    std::smatch matches; 

    if (std::regex_search(line, matches, pattern)) {
        std::string key = matches[1];
        std::string value = matches[2];
        
        if (project.comment.empty()) {
            project.comment += "\n" + value;
        }
        else {
            project.comment = value;
        }
    } else {
        std::cerr << "Regex failed: " << line << std::endl;
    }
}

static void handle_global_setting(Project& project, const std::string& line) {
    std::cout << "in handle_global_setting...\n";
}

static void handle_macro(Project& project, const std::string& line) {
    std::cout << "in handle_macro...\n";
}

static void handle_inst2a03(Project& project, const std::string& line){
    std::cout << "in handle_inst2a03...\n";
}

static void handle_instvrc6(Project& project, const std::string& line){
    std::cout << "in handle_instvrc6...\n";
}

static void handle_instvrc7(Project& project, const std::string& line){
    std::cout << "in handle_instvrc7...\n";
}

static void handle_instfds(Project& project, const std::string& line){
    std::cout << "in handle_instfds...\n";
}

static void handle_instn163(Project& project, const std::string& line) {
    std::cout << "in handle_instn163...\n";
}

static void handle_insts5b(Project& project, const std::string& line) {
    std::cout << "in handle_insts5b...\n";
}

static void handle_fdswave(Project& project, const std::string& line) {
    std::cout << "in handle_fdswave...\n";
}

static void handle_fdsmod(Project& project, const std::string& line) {
    std::cout << "in handle_fdsmod...\n";
}

static void handle_fdsmacro(Project& project, const std::string& line) {
    std::cout << "in handle_fdsmacro...\n";
}

static void handle_n163wave(Project& project, const std::string& line) {
    std::cout << "in handle_n163wave...\n";
}

static void handle_track(Project& project, const std::string& line) {
    std::cout << "in handle_track...\n";
}

static void handle_columns(Project& project, const std::string& line) {
    std::cout << "in handle_columns...\n";
}

static void handle_order(Project& project, const std::string& line) {
    std::cout << "in handle_order...\n";
}

static void handle_pattern(Project& project, const std::string& line) {
    std::cout << "in handle_pattern...\n";
}

static void handle_row(Project& project, const std::string& line) {
    std::cout << "in handle_row...\n";
}

static bool is_blank(const std::string& s) {
    return std::all_of(s.begin(), s.end(), [](unsigned char c) {
        return std::isspace(c);
    });
}

void scan_project(Project& project, const std::string file_path)
{
    std::cout << "[INFO] Scanning Project ---\n";

    static std::unordered_map<std::string, void(*)(Project&, const std::string&)> dtable = {
        // header methods
        {"TITLE",       &handle_song_info},
        {"AUTHOR",      &handle_song_info},
        {"COPYRIGHT",   &handle_song_info},
        {"COMMENT",     &handle_comment},

        {"MACHINE", &handle_global_setting},
        {"FRAMERATE", &handle_global_setting},
        {"EXPANSION", &handle_global_setting},
        {"VIBRATO", &handle_global_setting},
        {"SPLIT", &handle_global_setting},
        {"N163CHANNELS" , &handle_global_setting},
        
        // macro methods
        {"MACRO",       &handle_macro},
        {"MACROVRC6",   &handle_macro},
        {"MACRON163",   &handle_macro},
        {"MACROS5B",    &handle_macro},
        // instrument methods
        {"INST2A03", &handle_inst2a03},
        {"INSTVRC6", &handle_instvrc6},
        {"INSTVRC7", &handle_instvrc7},
        {"INSTFDS", &handle_instfds},
        {"INSTN163", &handle_instn163},
        {"INSTS5B", &handle_insts5b},
        // special methods
        {"FDSWAVE", &handle_fdswave},
        {"FDSMOD", &handle_fdsmod},
        {"FDSMACRO", &handle_fdsmacro},
        {"N163WAVE", &handle_n163wave},
        // track methods
        {"TRACK", &handle_track}, 
        {"COLUMNS", &handle_columns}, 
        {"ORDER", &handle_order}, 
        {"PATTERN", &handle_pattern}, 
        {"ROW", &handle_row}
    };

    std::ifstream input_file(file_path);

    if (!input_file.is_open()) {
        std::cerr << "Error: Could not open file" << std::endl; 
        return;
    }
    
    std::string line; 
    std::stringstream ss; 
    std::string first_word;

    while (std::getline(input_file, line)) {
        // std::cout << "Line: " << line << std::endl;
        
        if (line.empty()) continue;
        if (is_blank(line)) continue; 
        if (line[0] == '#') continue;
        
        std::cout << "[D] " << line << std::endl;

        std::stringstream ss(line);
        first_word.clear();
        ss >> first_word;
        
        auto it = dtable.find(first_word);
        if (it != dtable.end()) {
            // std::cout << "Found method: " << first_word << std::endl;
            (it->second)(project, line);
        } else {
            std::cout << "No match in dtable: " << first_word << std::endl;
        }
    }

    std::cout << "********************************************************************************\n";
    project_say(project);
}

void format_project(Project& project)
{
    std::cout << "[INFO] formatting project ...\n";
}

void export_midi(Project& project, const std::string& output_file)
{
    std::cout << "[INFO] exporting project...\n";
}

void project_say(const Project& project) {
    std::cout << "--- Project --- \n";
    
    std::cout << "--- Song Information ---\n";
    std::cout << "title => " << project.title << "\n";
    std::cout << "author => " << project.author << "\n";
    std::cout << "copyright => " << project.copyright << "\n";
    std::cout << "comment => " << project.comment << "\n";

    std::cout << "\n--- Global Settings ---\n";
    std::cout << "machine => " << project.machine << "\n";
    std::cout << "framerate => " << project.framerate << "\n";
    std::cout << "expansion => " << project.expansion << "\n";
    std::cout << "vibrato => " << project.vibrato << "\n";
    std::cout << "split => " << project.split << "\n";
    std::cout << "n163channels; => " << project.n163channels << "\n";
}