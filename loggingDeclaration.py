import logging
from datetime import datetime

class Logger:
    # Define log levels
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    INFO2 = 25  # Custom log level between INFO and DEBUG
    DEBUG = logging.DEBUG
    DEBUG1 = 15
    DEBUG2 = 14
    DEBUG3 = 13
    DEBUG4 = 12

    # Set default reporting level
    _reporting_level = INFO2

    def __init__(self):
        """
        Initialize the Logger object with an empty message.
        """
        self.message_level = None
        self.message = []

    def get(self, level):
        """
        Start building a log message at the specified level.
        """
        self.message_level = level
        return self

    def write(self, msg):
        """
        Append a message to the log entry.
        """
        self.message.append(str(msg))

    def flush(self):
        """
        Output the message if its level is within the reporting level.
        """
        if self.message_level <= Logger._reporting_level:
            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_level = self._level_to_string(self.message_level)
            print(f"{log_time} [{log_level}] {' '.join(self.message)}")

    @staticmethod
    def reporting_level():
        """
        Get the current reporting level.
        """
        return Logger._reporting_level

    @staticmethod
    def set_reporting_level(level):
        """
        Set the reporting level to control which messages are logged.
        """
        Logger._reporting_level = level

    @staticmethod
    def _level_to_string(level):
        """
        Convert a log level integer to a human-readable string.
        """
        level_map = {
            Logger.CRITICAL: "CRITICAL",
            Logger.ERROR: "ERROR",
            Logger.WARNING: "WARNING",
            Logger.INFO: "INFO",
            Logger.INFO2: "INFO2",
            Logger.DEBUG: "DEBUG",
            Logger.DEBUG1: "DEBUG1",
            Logger.DEBUG2: "DEBUG2",
            Logger.DEBUG3: "DEBUG3",
            Logger.DEBUG4: "DEBUG4",
        }
        return level_map.get(level, "UNKNOWN")

# Add custom levels to Python logging (optional, for compatibility with other loggers)
logging.addLevelName(Logger.INFO2, "INFO2")
logging.addLevelName(Logger.DEBUG1, "DEBUG1")
logging.addLevelName(Logger.DEBUG2, "DEBUG2")
logging.addLevelName(Logger.DEBUG3, "DEBUG3")
logging.addLevelName(Logger.DEBUG4, "DEBUG4")
