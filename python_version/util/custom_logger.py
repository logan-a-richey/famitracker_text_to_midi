#!/usr/bin/env python3
# custom logger 

from types import MethodType 

class LoggingLevels:
    ''' Logging level values '''

    VERBOSE = 50
    DEBUG   = 40
    INFO    = 30
    WARN    = 20
    ERROR   = 10
    CRITICAL = 5


class Colors:
    ''' Linux Ansi text color scheme '''

    RED = "\033[91m"
    YELLOW = "\033[93m"
    GRAY = "\033[90m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    PINK = "\u001b[35m"
    CYAN = "\u001b[36m"


class Logger:
    ''' Simple custom logger with color formatting! '''

    def __init__(self, _name: str):
        self.name = _name
        
        self.level = LoggingLevels.DEBUG
        self.create_handlers()

    def set_level(self, level: int):
        self.level = level

    def create_handlers(self):
        fields = ["verbose", "debug", "info", "warn", "error", "critical"]
        
        levels = [
            LoggingLevels.VERBOSE,
            LoggingLevels.DEBUG,
            LoggingLevels.INFO,
            LoggingLevels.WARN,
            LoggingLevels.ERROR,
            LoggingLevels.CRITICAL
        ]
        
        level_colors = {
            "VERBOSE": Colors.CYAN,
            "DEBUG": Colors.CYAN,
            "INFO": Colors.WHITE,
            "WARN": Colors.YELLOW,
            "ERROR": Colors.RED,
            "CRITICAL": Colors.RED
        }

        def create_log_method(field, level):
            ''' Dynamically create a new logging method '''

            color = level_colors.get(field.upper(), Colors.RESET)
            def log_method(self, msg: str):
                if self.level >= level:
                    print("{}[{}] - {}{}".format(color, field.upper(), msg, Colors.RESET))
                return

            return log_method

        for field, level in zip(fields, levels):
            method = MethodType(create_log_method(field, level), self)
            setattr(self, field, method)
    
    # for intellisese / auto-complete developer experience
    def verbose(self, msg: str): pass
    def debug(self, msg: str): pass
    def info(self, msg: str): pass
    def warn(self, msg: str): pass
    def error(self, msg: str): pass
    def critical(self, msg: str): pass


if __name__ == "__main__":
    logger = Logger(__name__)
    
    msg = "Hello there. General Kenobi!"
    funcs = [
        logger.verbose,
        logger.debug,
        logger.info,
        logger.warn,
        logger.error,
        logger.critical
    ]
    for func in funcs:
        func(msg)


