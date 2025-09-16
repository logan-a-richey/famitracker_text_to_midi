#!/usr/bin/env python3
# midi_writer.py

# class designed to write MIDI files
# can support over 16 tracks per song

from typing import List, Tuple, Dict
import struct

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MIDI meta event constants
META_END_OF_TRACK = bytes([0xFF, 0x2F, 0x00])
META_TEMPO_PREFIX = bytes([0xFF, 0x51, 0x03])
META_TIME_SIGNATURE_PREFIX = bytes([0xFF, 0x58, 0x04])

class Track:
    def __init__(self):
        self.events: List[Tuple[int, bytes]] = []

    def add_event(self, tick: int, event_bytes: bytes):
        self.events.append((tick, event_bytes))

    def sort_events(self):
        self.events.sort(key=lambda e: e[0])


class MidiWriter:
    TICKS_PER_QUARTER = 480

    def __init__(self):
        self.tracks: List[Track] = []
        self.channel_program: Dict[int, int] = {}

    def add_track(self) -> int:
        self.tracks.append(Track())
        return len(self.tracks) - 1

    def _get_track(self, idx: int) -> Track:
        while idx >= len(self.tracks):
            self.add_track()
        return self.tracks[idx]

    def set_channel(self, channel: int, program: int):
        self.channel_program[channel] = program
        event = bytes([0xC0 | (channel & 0x0F), program & 0x7F])
        self._get_track(0).add_event(0, event)

    def add_bpm(self, track_idx: int, start: int, bpm: int):
        if bpm <= 0:
            logger.warning(f"Invalid BPM: {bpm}")
            return
        tempo = 60000000 // bpm
        tempo_bytes = tempo.to_bytes(3, 'big')
        event = META_TEMPO_PREFIX + tempo_bytes
        self._get_track(track_idx).add_event(start, event)

    def add_time_signature(self, track_idx: int, start: int, numerator: int, denominator: int):
        if numerator <= 0 or (denominator & (denominator -1)) != 0:
            logger.warning(f"Invalid time signature {numerator}/{denominator}")
            return
        dd = 0
        denom = denominator
        while denom > 1:
            denom >>= 1
            dd += 1
        cc = 24  # MIDI clocks per metronome click
        bb = 8   # number of 32nd notes per quarter
        event = META_TIME_SIGNATURE_PREFIX + bytes([numerator, dd, cc, bb])
        self._get_track(track_idx).add_event(start, event)

    def add_track_name(self, track_idx: int, name: str, start: int = 0):
        name_bytes = name.encode('ascii')
        event = bytes([0xFF, 0x03, len(name_bytes)]) + name_bytes
        self._get_track(track_idx).add_event(start, event)

    def add_note(self, track_idx: int, channel: int, start: int, duration: int,
                 pitch: int, velocity: int, off_velocity: int = 64):
        if duration <= 0:
            logger.error("Non-positive duration. You said {}".format(duration))
        if velocity <= 0 or velocity > 127:
            raise ValueError("Velocity OOB. You said {}".format(velocity))
        
        end = start + duration
        track = self._get_track(track_idx)
        note_on = bytes([0x90 | (channel & 0x0F), pitch & 0x7F, velocity & 0x7F])
        note_off = bytes([0x80 | (channel & 0x0F), pitch & 0x7F, off_velocity & 0x7F])
        track.add_event(start, note_on)
        track.add_event(end, note_off)

    def encode_var_len(self, value: int) -> bytes:
        buffer = []
        buffer.append(value & 0x7F)
        value >>= 7
        while value:
            buffer.append((value & 0x7F) | 0x80)
            value >>= 7
        buffer.reverse()
        return bytes(buffer)

    def save(self, filename: str):
        # Sort all events
        for track in self.tracks:
            track.sort_events()

        # MIDI header
        header = b'MThd' + struct.pack(
            ">IHHH",
            6,                  # header length
            1 if len(self.tracks) > 1 else 0,  # format type
            len(self.tracks),   # number of tracks
            self.TICKS_PER_QUARTER
        )

        output = bytearray(header)

        # Tracks
        for track in self.tracks:
            track_data = bytearray()
            last_tick = 0
            for tick, event in track.events:
                delta = tick - last_tick
                last_tick = tick
                track_data += self.encode_var_len(delta) + event
            # End of track event
            track_data += self.encode_var_len(0) + META_END_OF_TRACK
            # Track chunk header
            output += b'MTrk' + struct.pack(">I", len(track_data)) + track_data

        with open(filename, "wb") as f:
            f.write(output)
        logger.info(f"Saved MIDI file: {filename}")

