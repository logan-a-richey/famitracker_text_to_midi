# project_formatter.py

import re
from helpers.helper_functions import generate_token_key, get_next_item
from helpers.constants import TokenType, ControlFlowType
from helpers.regex_patterns import RegexPatterns
from data.echo_buffer import  EchoBuffer 


class ProjectFormatter:
    def __init__(self):
        self.track = None
        self.target_order = 0 
        self.target_row = 0
        self.list_orders = []
        self.echo_buffers = []

    def classify_token_type(self, token: str) -> int:
        matchers = [
            RegexPatterns.NOTE_ON,
            RegexPatterns.NOTE_OFF,
            RegexPatterns.NOTE_RELEASE,
            RegexPatterns.NOISE_ON,
            RegexPatterns.ECHO_BUFFER
        ]
        return_fields = [
            TokenType.NOTE_ON,
            TokenType.NOTE_OFF,
            TokenType.NOTE_RELEASE,
            TokenType.NOISE_ON,
            TokenType.ECHO_BUFFER
        ]
        
        # TODO - use zip instead
        for i in range(len(matchers)):
            regex_match = matchers[i].match(token)
            if regex_match:
                return return_fields[i]

        return TokenType.OTHER
    
    def handle_echo_buffer(self, token: str, col: int):
        echo_value = int(token[2])
        echo_token = self.echo_buffers[col].peek(echo_value)
        if not echo_token:
            return "{}{}".format("...", token[3:])
        
        return "{}{}".format(echo_token[:3], token[3:])

    def handle_control_flow(self, line: str):
        bxx_matches = RegexPatterns.BXX.findall(line)
        cxx_matches = RegexPatterns.CXX.findall(line)
        dxx_matches = RegexPatterns.DXX.findall(line)

        if cxx_matches:
            # self.target_order = self.target_order
            # self.target_row = self.target_row
            return ControlFlowType.CXX
        
        if bxx_matches:
            last_bxx_match = bxx_matches[-1]
            bxx_value = int(last_bxx_match[1:], 16)
            if bxx_value in self.list_orders:
                self.target_order = bxx_value
            else:
                self.target_order = self.list_orders[-1]
            self.target_row = 0
            return ControlFlowType.BXX 
        
        if dxx_matches:
            last_dxx_match = dxx_matches[-1]
            dxx_value = int(last_dxx_match[1:], 16)
            dxx_value = max(0, dxx_value)
            dxx_value = min(dxx_value, self.track.num_rows - 1)

            next_order = get_next_item(self.list_orders, self.target_order)
            self.target_order = next_order
            self.target_row = dxx_value
            return ControlFlowType.DXX

        return ControlFlowType.OTHER
    
    def scan_target_order(self):
        pattern_list = self.track.orders[self.target_order]

        tokens = []
        for i in range(self.target_row, self.track.num_rows):
            tokens.clear()
            for j in range(self.track.num_cols):
                token_key = generate_token_key(pattern_list[j], i, j)
                token = self.track.tokens.get(token_key, None)
                if not token:
                    null_token = "... .. .{}".format("..." * self.track.eff_cols[j])
                    tokens.append(null_token)
                    continue

                event_type = self.classify_token_type(token)
                if event_type == TokenType.ECHO_BUFFER:
                    token = self.handle_echo_buffer(token, j)
                
                tokens.append(token)
            # end col
            
            line = " : ".join(tokens)
            self.track.lines.append(line)

            res = self.handle_control_flow(line)
            if res in [ControlFlowType.BXX, ControlFlowType.CXX, ControlFlowType.DXX]:
                return
            
        # end row            
        
        next_order = get_next_item(self.list_orders, self.target_order)
        self.target_order = next_order
        self.target_row = 0
        return

    def format_track(self, track):
        self.track = track
        self.track.lines.clear()

        self.list_orders = list(track.orders.keys())
        self.echo_buffers = [EchoBuffer() for _ in range(self.track.num_cols)]

        seen_it = set()
        while self.target_order not in seen_it:
            print("[INFO] Scanning order {}".format(self.target_order))

            seen_it.add(self.target_order)
            self.scan_target_order()
        return
    
    def format_project(self, project):
        for track in project.tracks:
            self.format_track(track)
        return
