// utils.h

#pragma once 

#include "project.h"

void scan_project(Project& project, const std::string input_file);

void format_project(Project& project);

void export_midi(Project& project, const std::string& output_file);

void project_say(const Project& project);