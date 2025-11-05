# FamiTracker Text To MIDI — Python Version

A Python application that converts a FamiTracker text export file (`.txt`) into a MIDI file.

MIDI files can then be imported into DAWs or notation software such as MuseScore or FL Studio, saving hours of manual transcription work.

---

## Features

* Builds a `Project` object to store all parsed FamiTracker data.
* `ProjectReader` parses the `.txt` export file line by line into structured data.
* Uses a **dynamic registry decorator** to implement a flexible dispatch table for opcode handling.
* Handles large input files (≈200,000 lines) efficiently — typically under 3 seconds.
* `ProjectFormatter` expands FamiTracker’s lightweight compression into sequential track lines.
* Includes a custom-built `MidiWriter` module for low-level MIDI event creation and binary writing.
* `ProjectExporter` converts sequential project data into playable MIDI tracks.
* Supports multi-song `.txt` files — automatically exports all tracks to separate `.mid` files.

---

## Technical Highlights

* Comprehensive use of Python’s standard library: `re`, `struct`, `io`, `dataclasses`, `pathlib`, and `typing`.
* Object-oriented design with clear separation between reader, parser, and exporter layers.
* Efficient token and pattern storage using Python dictionaries and comprehensions.
* In-depth handling of MIDI variable-length quantities, delta times, and binary chunk structures.
* Command-line interface for batch processing of multiple files.

---

## Installation & Usage

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### Run

```bash
python -m famitracker_to_midi <input_famitracker_file.txt> <output_directory (optional)>
```

This will create one or more `.mid` files corresponding to all songs in the FamiTracker export.

---

## Project Significance

This implementation emphasizes:

* Advanced file I/O and parsing in Python.
* OOP design patterns and registry-based dispatching.
* Hands-on experience with binary MIDI encoding.
* Managing an independent Git repository with disciplined version control practices.

---

## Next Steps

* Improve drum mapping heuristics between FamiTracker and General MIDI kits.
* Add support for MIDI → FamiTracker conversion.
* Develop a simple Flask-based web frontend (proof-of-concept SaaS tool for chiptune composers).

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

