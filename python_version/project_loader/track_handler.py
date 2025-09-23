# track_handler.py

import re
from helpers.regex_patterns import RegexPatterns
from project_loader.handler_registry import register
from data.track import Track
from helpers.helper_functions import generate_token_key

NULL_TOKEN = re.compile(r'^[\.\s]*$')

class TrackHandler:
    def __init__(self):
        # self.project_loader = project_loader 
        pass

    @register("TRACK")
    def handle_track(self, project, line):
        regex_match = RegexPatterns.TRACK.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        args = ["num_rows", "speed", "tempo"]
        num_rows, speed, tempo = list(map(int, regex_match.group(*args)))
        name = regex_match.group("name")

        t = Track( num_rows, speed, tempo, name)

        project.tracks.append(t)
    
    @register("COLUMNS")
    def handle_columns(self, project, line):
        regex_match = RegexPatterns.COLUMNS.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        t = project.tracks[-1]

        # TODO deo this in regex
        eff_cols = list(map(int, line.split(":")[1].strip().split()))
        num_cols = len(eff_cols)
        
        t.eff_cols = eff_cols
        t.num_cols = num_cols
    
    @register("ORDER")
    def handle_order(self, project, line):
        t = project.tracks[-1]
        
        field_key = line.split()[1]
        field_lst = line.split(":")[1].strip().split()
        key = int(field_key, 16)
        lst = list(map(lambda x: int(x, 16), field_lst))

        t.orders[key] = lst
    
    @register("PATTERN")
    def handle_pattern(self, project, line):
        # TODO deo this in regex
        field_pat = line.split()[1]
        self.current_pattern = int(field_pat, 16)
    
    @register("ROW")
    def handle_row(self, project, line):
        # TODO deo this in regex
        t = project.tracks[-1]
        
        row = int(line.split()[1], 16)
        tokens = [token.strip() for token in line.split(":")[1:]]

        for col, token in enumerate(tokens):
            # TODO check for null token
            null_token_match = NULL_TOKEN.match(token)
            if null_token_match:
                #print("NULL TOKEN: {}".format(token))
                continue

            token_key = generate_token_key(self.current_pattern, row, col)
            t.tokens[token_key] = token

