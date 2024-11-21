from datetime import datetime
from loggingDeclaration import Logger

# Map Logger levels to their string representations
TLoggerLevelToString = {
    Logger.CRITICAL: "LoggerCRITICAL",
    Logger.ERROR: "LoggerERROR",
    Logger.WARNING: "LoggerWARNING",
    Logger.INFO: "LoggerINFO",
    Logger.INFO2: "LoggerINFO2",
    Logger.DEBUG: "LoggerDEBUG",
    Logger.DEBUG1: "LoggerDEBUG1",
    Logger.DEBUG2: "LoggerDEBUG2",
    Logger.DEBUG3: "LoggerDEBUG3",
    Logger.DEBUG4: "LoggerDEBUG4",
}

# Global reporting level
globalMessageLevel = Logger.INFO2

# Function to return the current timestamp as a formatted string
def nowtime():
    """
    Get the current time formatted as "%F %T %z".
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")

# Set the reporting level in the Logger class
def reporting_level():
    """
    Get the current global reporting level.
    """
    return globalMessageLevel

Logger.set_reporting_level(reporting_level())

# Loggerging functionality wrapper
class LoggerWrapper(Logger):
    def get(self, level):
        """
        Start building a Logger message at the specified level.
        """
        timestamp = nowtime()
        Logger_level_str = TLoggerLevelToString.get(level, "UNKNOWN")
        self.message_level = level
        self.write(f"- {timestamp} {Logger_level_str}: ")
        return self

    def __del__(self):
        """
        Outputs the Logger message to `stderr` if the message level is within the reporting level.
        """
        if self.message_level <= Logger.reporting_level():
            self.flush()
