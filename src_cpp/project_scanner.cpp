// project_scanner.cpp 

#include "project_scanner.h" 

#include <iostream>
#include <fstream>
#include <regex> 
#include <unordered_map>
#include <sstream>

// *****************************************************************************
// Private Methods
// Helpers
bool ProjectScanner::is_blank(const std::string& s) {
    return std::all_of(s.begin(), s.end(), [](unsigned char c) {
        return std::isspace(c);
    });
}

std::string ProjectScanner::convert_line_to_ascii(const std::string& input){
    std::string output;
    std::copy_if(input.begin(), input.end(), std::back_inserter(output),
        [](unsigned char c) {
            return c == '\n' || (c >= 32 && c <= 126);
        });
    return output;
}

// *****************************************************************************
// Line Handlers 
void ProjectScanner::handle_song_info(Project& project, const std::string& line) {
    std::cout << "in handle_song_info...\n";

    // LINE
    // TITLE           "march bees test"
    // static const std::regex pattern(R"(^\s*(TITLE|AUTHOR|COPYRIGHT)\s+"(.*)".*$)");
    static const std::regex pattern("^\\s*(\\w+)\\s+\"(.*)\"$");
    std::smatch matches; 

    if (std::regex_search(line, matches, pattern)) {
        std::string key = matches[1];
        std::string value = matches[2];

        if (key == "TITLE") project.title = value;
        else if (key == "AUTHOR") project.author = value; 
        else if (key == "COPYRIGHT") project.copyright = value;
    } else {
        std::cerr << "Regex failed: " << line << std::endl;
    }
}

void ProjectScanner::handle_comment(Project& project, const std::string& line) {
    std::cout << "in handle_comment...\n";
    
    static const std::regex pattern("^\\s*(\\w+)\\s+\"(.*)\"$");
    std::smatch matches; 

    if (std::regex_search(line, matches, pattern)) {
        std::string key = matches[1];
        std::string value = matches[2];
        
        if (!project.comment.empty()) project.comment += "\n" + value;
        else project.comment = value;

    } else {
        std::cerr << "Regex failed: " << line << std::endl;
    }
}

void ProjectScanner::handle_global_setting(Project& project, const std::string& line) {
    std::cout << "in handle_global_setting...\n";
}

void ProjectScanner::handle_macro(Project& project, const std::string& line) {
    std::cout << "in handle_macro...\n";
}

void ProjectScanner::handle_inst2a03(Project& project, const std::string& line){
    std::cout << "in handle_inst2a03...\n";
}

void ProjectScanner::handle_instvrc6(Project& project, const std::string& line){
    std::cout << "in handle_instvrc6...\n";
}

void ProjectScanner::handle_instvrc7(Project& project, const std::string& line){
    std::cout << "in handle_instvrc7...\n";
}

void ProjectScanner::handle_instfds(Project& project, const std::string& line){
    std::cout << "in handle_instfds...\n";
}

void ProjectScanner::handle_instn163(Project& project, const std::string& line) {
    std::cout << "in handle_instn163...\n";
}

void ProjectScanner::handle_insts5b(Project& project, const std::string& line) {
    std::cout << "in handle_insts5b...\n";
}

void ProjectScanner::handle_fdswave(Project& project, const std::string& line) {
    std::cout << "in handle_fdswave...\n";
}

void ProjectScanner::handle_fdsmod(Project& project, const std::string& line) {
    std::cout << "in handle_fdsmod...\n";
}

void ProjectScanner::handle_fdsmacro(Project& project, const std::string& line) {
    std::cout << "in handle_fdsmacro...\n";
}

void ProjectScanner::handle_n163wave(Project& project, const std::string& line) {
    std::cout << "in handle_n163wave...\n";
}

void ProjectScanner::handle_track(Project& project, const std::string& line) {
    std::cout << "in handle_track...\n";
}

void ProjectScanner::handle_columns(Project& project, const std::string& line) {
    std::cout << "in handle_columns...\n";
}

void ProjectScanner::handle_order(Project& project, const std::string& line) {
    std::cout << "in handle_order...\n";
}

void ProjectScanner::handle_pattern(Project& project, const std::string& line) {
    std::cout << "in handle_pattern...\n";
}

void ProjectScanner::handle_row(Project& project, const std::string& line) {
    std::cout << "in handle_row...\n";
}


//******************************************************************************
// Public Methods

void ProjectScanner::scan_project(Project& project, const std::string file_path)
{
    std::cout << "[INFO] Scanning Project ---\n";

    using fptr = void(ProjectScanner::*)(Project&, const std::string&);

    static std::unordered_map<std::string, fptr> dtable = {
        // song information
        {"TITLE", &ProjectScanner::handle_song_info},
        {"AUTHOR", &ProjectScanner::handle_song_info},
        {"COPYRIGHT", &ProjectScanner::handle_song_info},
        {"COMMENT", &ProjectScanner::handle_comment},
        
        // global settings
        {"MACHINE", &ProjectScanner::handle_global_setting},
        {"FRAMERATE", &ProjectScanner::handle_global_setting},
        {"EXPANSION", &ProjectScanner::handle_global_setting},
        {"VIBRATO", &ProjectScanner::handle_global_setting},
        {"SPLIT", &ProjectScanner::handle_global_setting},
        {"N163CHANNELS" , &ProjectScanner::handle_global_setting},

        // macro methods
        {"MACRO", &ProjectScanner::handle_macro},
        {"MACROVRC6", &ProjectScanner::handle_macro},
        {"MACRON163", &ProjectScanner::handle_macro},
        {"MACROS5B", &ProjectScanner::handle_macro},
        // instrument methods
        {"INST2A03", &ProjectScanner::handle_inst2a03},
        {"INSTVRC6", &ProjectScanner::handle_instvrc6},
        {"INSTVRC7", &ProjectScanner::handle_instvrc7},
        {"INSTFDS", &ProjectScanner::handle_instfds},
        {"INSTN163", &ProjectScanner::handle_instn163},
        {"INSTS5B", &ProjectScanner::handle_insts5b},
        // special methods
        {"FDSWAVE", &ProjectScanner::handle_fdswave},
        {"FDSMOD", &ProjectScanner::handle_fdsmod},
        {"FDSMACRO", &ProjectScanner::handle_fdsmacro},
        {"N163WAVE", &ProjectScanner::handle_n163wave},
        // track methods
        {"TRACK", &ProjectScanner::handle_track}, 
        {"COLUMNS", &ProjectScanner::handle_columns}, 
        {"ORDER", &ProjectScanner::handle_order}, 
        {"PATTERN", &ProjectScanner::handle_pattern}, 
        {"ROW", &ProjectScanner::handle_row}
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
            
            (this->*(it->second))(project, convert_line_to_ascii(line) );
        } else {
            std::cout << "No match in dtable: " << first_word << std::endl;
        }
    }
}
