# helper_functions.py

import re
from helpers.constants import TokenType 
from helpers.regex_patterns import RegexPatterns 

def generate_macro_key(_inst_type: int, _macro_type: int, _macro_index: int):
    ''' Used for macro token lookup during Project and Instrument creation and usage. '''
    
    # return "{}::{}::{}".format(_inst_type, _macro_type, _macro_index)
    return tuple([_inst_type, _macro_type, _macro_index])


def generate_token_key(pat, row, col):
    ''' Used for string token lookup during Track creation and usage. '''

    return tuple([pat, row, col])


def get_next_item(lst, item):
    ''' Get the next item of a list, given an item. Loop-around. '''
    
    if item not in lst:
        raise ValueError("Item not in list.")
    
    this_index = lst.index(item)
    next_index = (this_index + 1) % len(lst)
    return lst[next_index]

def clean_string(input_string, mode="Snake") -> str:
    ''' 
    Removes all non-alphanumeric chars from a string
    Converts to snake_case
    '''

    WORD_REGEX = re.compile(r'[a-zA-Z0-9]+') 
    if mode == "Pascal":
        word_list = WORD_REGEX.findall(input_string)
        word_list = [word.capitalize() for word in word_list]
        output_string = "".join(word_list)
        return output_string 
    else:
        word_list = WORD_REGEX.findall(input_string)
        word_list = [word.lower() for word in word_list]
        output_string = "_".join(word_list)
        return output_string 


def classify_token_type(token: str) -> int:
    '''
    Returns the corresponding event type of a FamiTracker note token.
    
    EVENT_TYPE:     | STRING        | STRING DESCRIPTION
    ----------------+---------------+---------------------------------------
    NOTE_ON:        | A-4, C#5, Bb4 | Note letter, accidental, octave
    NOTE_OFF:       | ---           | 3 dashes 
    NOTE_RELEASE:   | ===           | 3 equals
    NOTE_NOISE:     | #-0, #-F      | # - hex
    ECHO_BUFFER:    | ^-0, ^-3      | ^ - number
    OTHER:          | ..., xyz      | ... or invalid
    '''
    
    matchers = [
        RegexPatterns.NOTE_ON,
        RegexPatterns.NOTE_OFF,
        RegexPatterns.NOTE_RELEASE,
        RegexPatterns.NOISE_ON,
        RegexPatterns.ECHO_BUFFER
    ]
    fields = [
        TokenType.NOTE_ON,
        TokenType.NOTE_OFF,
        TokenType.NOTE_RELEASE,
        TokenType.NOISE_ON,
        TokenType.ECHO_BUFFER
    ]
    
    for matcher, field in zip(matchers, fields):
        regex_match = matcher.match(token)
        if regex_match:
            return field

    return TokenType.OTHER

NOTE_OFFSETS = { 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11 }
def get_midi_pitch(token: str) -> int:
    note_on_match = RegexPatterns.NOTE_ON.match(token)
    noise_on_match = RegexPatterns.NOISE_ON.match(token)

    if note_on_match:
        pitch = NOTE_OFFSETS.get(token[0], 0)

        accidental = token[1]
        if accidental == '#':
            pitch += 1
        elif accidental == 'b':
            pitch -= 1

        octave = int(token[2])
        pitch += octave * 12
        return pitch
    elif noise_on_match:
        pitch = int(token[0], 16)
        return pitch
    else:
        raise ValueError("Could not convert token to Midi pitch: {}".format(token))