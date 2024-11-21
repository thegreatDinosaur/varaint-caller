import logging
from datetime import datetime

class Log:
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
        Initialize the Log object with an empty message.
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
        if self.message_level <= Log._reporting_level:
            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_level = self._level_to_string(self.message_level)
            print(f"{log_time} [{log_level}] {' '.join(self.message)}")

    @staticmethod
    def reporting_level():
        """
        Get the current reporting level.
        """
        return Log._reporting_level

    @staticmethod
    def set_reporting_level(level):
        """
        Set the reporting level to control which messages are logged.
        """
        Log._reporting_level = level

    @staticmethod
    def _level_to_string(level):
        """
        Convert a log level integer to a human-readable string.
        """
        level_map = {
            Log.CRITICAL: "CRITICAL",
            Log.ERROR: "ERROR",
            Log.WARNING: "WARNING",
            Log.INFO: "INFO",
            Log.INFO2: "INFO2",
            Log.DEBUG: "DEBUG",
            Log.DEBUG1: "DEBUG1",
            Log.DEBUG2: "DEBUG2",
            Log.DEBUG3: "DEBUG3",
            Log.DEBUG4: "DEBUG4",
        }
        return level_map.get(level, "UNKNOWN")

# Add custom levels to Python logging (optional, for compatibility with other loggers)
logging.addLevelName(Log.INFO2, "INFO2")
logging.addLevelName(Log.DEBUG1, "DEBUG1")
logging.addLevelName(Log.DEBUG2, "DEBUG2")
logging.addLevelName(Log.DEBUG3, "DEBUG3")
logging.addLevelName(Log.DEBUG4, "DEBUG4")

# Example usage
log = Log()
log.set_reporting_level(Log.DEBUG)

# Log a message
logger = log.get(Log.INFO)
logger.write("This is an info-level message.")
logger.flush()

# Log a debug-level message
logger = log.get(Log.DEBUG)
logger.write("This is a debug-level message.")
logger.flush()

# Change reporting level
log.set_reporting_level(Log.WARNING)

# This won't print because it's below the reporting level
logger = log.get(Log.INFO)
logger.write("This info message will not be shown.")
logger.flush()

# This will print because it's at the warning level
logger = log.get(Log.WARNING)
logger.write("This is a warning-level message.")
logger.flush()
