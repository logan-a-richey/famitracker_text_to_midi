# Famitracker Text To Midi
Program to convert a FamiTracker text export file into a MIDI file.
MIDI files can be loaded into other software such as MuseScore or FL Studio, saving hours of manual transcription time.

## Features:
*   Creates a `Project` data structure to contain the data. 
*   `ProjectReader` reads the file line by line, loading data into the Project class.
*   Can process large files containing ~200,000 lines in under 3 seconds.
*   The Project is then parsed to create sequential lines. FamiTracker uses a light compression technique when storing tokens within patterns. The `ProjectFormatter` class unpacks those tokens.
*   Contains built-in `MidiWriter` submodule, a custom library written in both C++ and Python for creating MIDI files.
*   `ProjectExporter` reads the sequential line data and creates the MIDI track.
*   A FamiTracker module can contain many songs. This program will export all tracks in the file.

## Project Significance:
This unique project taught me much about Python and C++. Here are some of the key skills used throughout this project:
*   File I/O in both Python and C++.
*   Gained better understanding list comprehensions and `std::iterator` objects. 
*   String parsing with regex and `std::stringstream`.
*   Experienced with OOP data structures such as structs, dispatch tables, GoF design patterns, abstract classes as interfaces, standard library containers. 
*   Usage of Python's `dictionary` and C++'s `std::unordered_map<>` objects to store FamiTracker tokens and orders in a concise way.
*   Low-level binary parsing with MidiWriter. Parsing MIDI chunks of varying size (`varlen`), storing intermediate results in a Track object, writing the intermediate data to a MIDI binary file.
*   CMake build configurations.
*   Managing GitHub repos. Keeping effective version control through spliting and merging different branches, creating submodules, and merging and splitting multiple repos.

## Usage:

** Setup: **
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

** Run the app: **
`./app.exe <input_famitracker_file.txt> <output_directory (optional)`

## Next Steps:
* Smarter FamiTracker to MIDI drum mapping.
* Converting the other way: MIDI -> Famitracker.
* Flask web app version, demonstrating a simple SAAS application for any chiptune artists wishing to convert their .ftm files to .mid.
* Exploring template metaprogrmaming implementation of the dispatch table for compile-time results, though it is probably not needed for this project.

## License
The MIT License (MIT)

Copyright (c) 2025 LoganARichey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

