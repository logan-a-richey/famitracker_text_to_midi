#!/usr/bin/env python3

from midi_writer import MidiWriter 

def twinkle_star_test():
    FNAME1 = "py_twinkle_star.mid"
    LETTER_TO_PITCH = {
        'C': 60, 
        'D': 62, 
        'E': 64, 
        'F': 65,
        'G': 67, 
        'A': 69, 
        'B': 71
    }
    
    midi_writer = MidiWriter()
    midi_writer.add_bpm(0, 0, 120)
    midi_writer.add_time_signature(0, 0, 3, 4)
    
    beat = 0
    melody = "CCGGAAG_FFEEDDC_GGFFEED_GGFFEED_CCGGAAG_FFEEDDC_";
    for note_char in melody:
        if note_char == '_':
            beat += 1
            continue
        note_pitch = LETTER_TO_PITCH.get(note_char, 60)
        midi_writer.add_note(0, 0, 480 * beat, 480, note_pitch, 120)
        beat += 1
    
    midi_writer.save(FNAME1)
    print("[INFO] File created: {}".format(FNAME1))

def test():
    midi = MidiWriter()
    track_idx = midi.add_track()
    midi.set_channel(0, 1)  # channel 0, program 1 (e.g., piano)
    midi.add_bpm(track_idx, 0, 120)
    midi.add_time_signature(track_idx, 0, 4, 4)
    midi.add_note(track_idx, 0, 0, 480, 60, 100)  # C4, quarter note, velocity 100
    midi.save("output.mid")

def main():
    test()
    twinkle_star_test()

if __name__ == "__main__":
    main()
