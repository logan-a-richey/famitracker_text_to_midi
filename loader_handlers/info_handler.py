# info_handler.py

from handler_registry import register 
from regex_patterns import RegexPatterns

class InfoHandler(self):
    def __init__(self, parent_handler):
        self.parent = parent_handler

    @register("TITLE")
    @register("AUTHOR")
    @register("COPYRIGHT")
    def handle_song_information(self, project, line):
        ''' 
        Handle TITLE, AUTHOR, and COPYRIGHT metadata 
        Comment string is overwritten.
        '''
        regex_match = RegexPatterns.SONG_INFORMATION.match(line)
        if not regex_match:
            raise ValueError("Regex failed")

        key, val = regex_match.group("tag", "name")
        key = key.lower()

        if not hasattr(self.project, key):
            raise ValueError("Invalid SongInformation key.")

        setattr(self.project, key, val)

    @register("COMMENT")
    def handle_song_information(self, project, line):
        ''' 
        Handle COMMENT metadata.
        Comment string is appended.
        '''
        regex_match = RegexPatterns.SONG_INFORMATION.match(line)
        if not regex_match:
            raise ValueError("Regex failed.")
        
        key, val = regex_match.group("tag", "name")
        if self.project.comment:
            self.project.comment += "\n{}".format(val)
        else:
            self.project.comment = val

    @register("MACHINE")
    @register("FRAMERATE=")
    @register("EXPANSION=")
    @register("VIBRATO")
    @register("SPLIT")
    @register("N163CHANNELS")
    def handle_global_settings(self, project, line: str):
        ''' 
        Handle MACHINE, FRAMERATE, EXPANSION, VIBRATO, SPLIT, N163CHANNELS metadata. 
        Value is typecast to integer and Project data is overwritten.
        '''
        regex_match = RegexPatterns.GLOBAL_SETTINGS.match(line)
        if not regex_match:
            raise ValueError("Regex failed")

        key, val = regex_match.group("tag", "value")
        key = key.lower()
        val = int(val)

        if not hasattr(self.project, key):
            raise ValueError("Invalid GlobalSettings key.")

        setattr(self.project, key, val)

        pass

