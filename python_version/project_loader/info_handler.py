# info_handler.py

from project_loader.handler_registry import register 
from helpers.regex_patterns import RegexPatterns

class InfoHandler:
    def __init__(self):
        pass

    @register("TITLE")
    @register("AUTHOR")
    @register("COPYRIGHT")
    # def handle_song_information(self, project: "Project", line: str):
    def handle_song_information(self, project, line: str):
        ''' 
        Handle TITLE, AUTHOR, and COPYRIGHT metadata 
        Comment string is overwritten.
        '''
        regex_match = RegexPatterns.SONG_INFORMATION.match(line)
        if not regex_match:
            raise ValueError("{} Regex failed.".format(self.__class__.__name__))

        key, val = regex_match.group("tag", "name")
        key = key.lower()

        if not hasattr(project, key):
            raise ValueError("Invalid SongInformation key.")

        setattr(project, key, val)

    @register("COMMENT")
    # def handle_song_information(self, project: "Project", line: str):
    def handle_song_comment(self, project, line: str):
        ''' 
        Handle COMMENT metadata.
        Comment string is appended.
        '''
        regex_match = RegexPatterns.SONG_INFORMATION.match(line)
        if not regex_match:
            raise ValueError("{} Regex failed.".format(self.__class__.__name__))
        
        key, val = regex_match.group("tag", "name")
        if project.comment:
            project.comment += "\n{}".format(val)
        else:
            project.comment = val

    @register("MACHINE")
    @register("FRAMERATE")
    @register("EXPANSION")
    @register("VIBRATO")
    @register("SPLIT")
    @register("N163CHANNELS")
    # def handle_global_settings(self, project: "Project", line: str):
    def handle_global_settings(self, project, line: str):
        ''' 
        Handle MACHINE, FRAMERATE, EXPANSION, VIBRATO, SPLIT, N163CHANNELS metadata. 
        Value is typecast to integer and Project data is overwritten.
        '''
        regex_match = RegexPatterns.GLOBAL_SETTINGS.match(line)
        if not regex_match:
            raise ValueError("{} Regex failed.".format(self.__class__.__name__))

        key, val = regex_match.group("tag", "value")
        key = key.lower()
        val = int(val)

        if not hasattr(project, key):
            raise ValueError("Invalid GlobalSettings key.")

        setattr(project, key, val)

