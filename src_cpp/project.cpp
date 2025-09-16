// project.cpp

#include "project.h"

#include <iostream>

void Project::say() {
    std::cout << "--- Project --- \n";
    
    std::cout << "--- Song Information ---\n";
    std::cout << "title => " << title << "\n";
    std::cout << "author => " << author << "\n";
    std::cout << "copyright => " << copyright << "\n";
    std::cout << "comment => " << comment << "\n";

    std::cout << "\n--- Global Settings ---\n";
    std::cout << "machine => " << machine << "\n";
    std::cout << "framerate => " << framerate << "\n";
    std::cout << "expansion => " << expansion << "\n";
    std::cout << "vibrato => " << vibrato << "\n";
    std::cout << "split => " << split << "\n";
    std::cout << "n163channels; => " << n163channels << "\n";
}
