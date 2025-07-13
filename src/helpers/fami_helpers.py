# fami_helpers.py

class FamiHelpers:
    ''' Contains FamiTracker specific helper functions '''

    NOTE_OFFSETS = { 
        'C': 0, 
        'D': 2, 
        'E': 4, 
        'F': 5, 
        'G': 7, 
        'A': 9, 
        'B': 11 
    }

    @staticmethod 
    def get_fami_bpm(project: "Project", track: "Track") -> int:
        speed = max(track.speed, 1)
        #if track.index in project.usegroove:
        #    list_grooves = list(project.grooves.keys())
        #    first_groove_index = list_grooves[0]
        #    default_groove = project.grooves[first_groove_index]
        #    average_speed = sum(default_groove.data) / len(default_groove.data)
        bpm = int(track.tempo * (6 / speed))
        return bpm 
    
    @staticmethod 
    def get_note_on_pitch(token: str) -> int:
        try:
            pitch = FamiHelpers.NOTE_OFFSETS.get(token[0], 0)
            accidental = token[1]
            
            if accidental == '#':
                pitch += 1
            elif accidental == 'b':
                pitch -= 1

            # Add by 1: octave transposed. Make sure Middle C has pitch of 60
            octave = int(token[2]) + 1 
            pitch += octave * 12
            return pitch
        except:
            raise ValueError("Could not convert token to Midi pitch: {}".format(token))

    @staticmethod 
    def get_noise_on_pitch(token: str) -> int:
        try:
            pitch = int(token[0], 16) + 60
            return pitch
        except:
            raise ValueError("Could not convert token to Midi pitch: {}".format(token))

    @staticmethod 
    def get_token_inst(token: str, context: "ColContext") -> int:
        try: 
            return int(token.split()[1], 16)
        except:
            return context.last_inst

    @staticmethod 
    def get_token_vol(token: str, context: "ColContext") -> int:
        try: 
            return int(token.split()[2], 16) * 8
        except:
            return context.last_vol