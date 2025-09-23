# project_formatter.py

from util.custom_logger import Logger, LoggingLevels
logger = Logger(__name__)
logger.set_level(LoggingLevels.INFO)

import re
from helpers.helper_functions import generate_token_key, get_next_item, classify_token_type
from helpers.constants import TokenType, ControlFlowType
from helpers.regex_patterns import RegexPatterns
from data.echo_buffer import  EchoBuffer 


class ProjectFormatter:
    def __init__(self):
        ''' 
        Stores Track state while formatting.
        Famitracker Orders are denoted by:
        ORDER aa : bb cc dd ... (where aa, bb, cc, dd, etc. are base16 numbers)
        aa is the order number.
        order aa contain columns from other orders:
        bb represents the token col from order bb.         
        cc represents the token col from order cc. and so on...
        there is a variadic number of columns denoted by the COLUMNS section in the Famitracker text export.

        Steps:
        - Loop over tracks in a project
        - Scan orders in a track, starting at order 0 (order hex are already stored as unsigned int)
        - Build the line by looping over rows and cols. We can search up the substrings from the tokens stored in Track.
        - If a token is an echo event (^-X) then replace the token with the correct substring.
        - Append token substring to EchoBuffer as needed. (Append if note is of type: ON, OFF, ECHO, or NOISE.)
        - Build the line of tokens and append it to Track.lines.
        - If a line contains bxx, cxx, dxx, handle the order skip event properly. (Note we handle this event after we append the current line to Track.)
        - Continue this process until we have reached a target order we have seen already.
        
        Now the lines are in sequential order, and are ready to be parsed by the MidiExporter.
        '''

        self.track = None
        self.target_order = 0 
        self.target_row = 0
        self.list_orders = []
        self.echo_buffers = []

    
    def handle_echo_buffer(self, token: str, col: int) -> str:
        ''' 
        Given that token is an EchoBuffer event, replace ^-X with the correct substring from EchoBuffer 
        If there is no valid substring, replace ^-X will a null token "..."
        Return the updated substring.
        '''

        echo_value = int(token[2])
        echo_token = self.echo_buffers[col].peek(echo_value)
        if not echo_token:
            return "{}{}".format("...", token[3:])
        
        return "{}{}".format(echo_token[:3], token[3:])

    def handle_control_flow(self, line: str):
        '''
        BXX, CXX, and DXX effects can cause the Track to jump around in the score.
        BXX will go to Order XX at Row 0. If XX is not a valid order, go to last Order.
        CXX ends the song. We simply return. The seen_it loop will cause the song to end.
        DXX goes to the next Order at Row XX. Row XX is bounded between 0 and num_rows - 1.
        If no match, return and continue scanning the order as usual.
        '''

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
        '''
        Scan an order starting from `self.target_row` to `self.track.num_rows`.
        Build up a list of tokens. Combine them into a line string and append it to `self.track`.
        Handles echo buffer and order skip events within line.
        '''
        
        pattern_list = self.track.orders[self.target_order]

        tokens = []
        for i in range(self.target_row, self.track.num_rows):
            tokens.clear()
            for j in range(self.track.num_cols):
                token_key = generate_token_key(pattern_list[j], i, j)
                token = self.track.tokens.get(token_key, None)
                if not token:
                    null_token = "... .. .{}".format(" ..." * self.track.eff_cols[j])
                    tokens.append(null_token)
                    continue

                event_type = classify_token_type(token)
                if event_type == TokenType.ECHO_BUFFER:
                    token = self.handle_echo_buffer(token, j)

                if event_type in [TokenType.NOISE_ON, TokenType.NOTE_OFF, TokenType.NOTE_ON, TokenType.ECHO_BUFFER]:
                    self.echo_buffers[j].push_front(token[:3])

                tokens.append(token)
            prefix = "PAT {:02x} ROW {:02x}".format(self.target_order, i)
            prefix = prefix.upper()

            line = " | ".join([prefix] + tokens)

            self.track.lines.append(line)

            res = self.handle_control_flow(line)
            if res in [ControlFlowType.BXX, ControlFlowType.CXX, ControlFlowType.DXX]:
                return
            
        next_order = get_next_item(self.list_orders, self.target_order)
        self.target_order = next_order
        self.target_row = 0

    def format_track(self, track):
        ''' Populates track.lines with the correct seqential data '''

        # setup
        self.track = track
        self.track.lines.clear()

        self.list_orders = list(track.orders.keys())
        self.echo_buffers = [EchoBuffer() for _ in range(self.track.num_cols)]

        # loop over song
        seen_it = set()
        while self.target_order not in seen_it:
            seen_it.add(self.target_order)
            self.scan_target_order()

        # Add final line (Needed for final note append. Note OFF will trigger it)
        final_tokens = []
        for col in self.track.eff_cols:
            token = "--- .. .{}".format(" ..." * col) 
            final_tokens.append(token)
        
        stop_line = " | ".join(["PAT XX ROW XX"] + final_tokens)
        self.track.lines.append(stop_line)        

        #for line in track.lines:
        #    logger.verbose(line)
    
    def format_project(self, project):
        ''' Formats all Tracks within a Project '''

        for track in project.tracks:
            self.format_track(track)
        
