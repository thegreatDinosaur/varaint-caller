import locale
import re
from enum import Enum
from typing import Optional, List, TypeVar, Iterable

# Type variable for generic type
T = TypeVar('T')

# Function to read an optional value
def read_optional(value: Optional[T]) -> Optional[T]:
    return value

# String splitting function
def split(s: str, delim: str) -> List[str]:
    if not s:
        return [""]
    return s.split(delim)

# Join function
def join(v: Iterable[str], delim: str = ",") -> str:
    return delim.join(v)

# Reverse join function
def rjoin(v: List[str], delim: str = ",") -> str:
    return delim.join(reversed(v))

# Trim whitespace from the left of the string
def ltrim(s: str) -> str:
    return s.lstrip()

# Trim specified characters from the left of the string
def ltrim_with_filter(s: str, filter_chars: str) -> str:
    return s.lstrip(filter_chars)

# Trim whitespace from the right of the string
def rtrim(s: str) -> str:
    return s.rstrip()

# Trim specified characters from the right of the string
def rtrim_with_filter(s: str, filter_chars: str) -> str:
    return s.rstrip(filter_chars)

# Trim whitespace from both sides of the string
def trim(s: str) -> str:
    return s.strip()

# Trim specified characters from both sides of the string
def trim_with_filter(s: str, filter_chars: str) -> str:
    return s.strip(filter_chars)

# Make a copy of the string and trim it
def trim_copy(s: str) -> str:
    return trim(s)

# Make a copy of the string and trim it with specified filter characters
def trim_copy_with_filter(s: str, filter_chars: str) -> str:
    return trim_with_filter(s, filter_chars)

# Format a help string with a name and description, aligned to a specified width
def format_help(name: str, description: str, width: int) -> str:
    name = "  " + name
    if len(name) >= width:
        formatted = f"{name}\n{' ' * width}{description}"
    else:
        formatted = f"{name:<{width}}{description}"
    return formatted

# Verify the first character of an option
def valid_first_char(c: str) -> bool:
    return c.isalpha() or c == '_'

# Verify following characters of an option
def valid_later_char(c: str) -> bool:
    return c.isalnum() or c in {'_', '.', '-'}

# Verify an option name
def valid_name_string(s: str) -> bool:
    if not s or not valid_first_char(s[0]):
        return False
    return all(valid_later_char(c) for c in s[1:])

# Return a lower case version of a string
def to_lower(s: str) -> str:
    return s.lower()

# Remove underscores from a string
def remove_underscore(s: str) -> str:
    return s.replace('_', '')

# Find and replace a substring with another substring
def find_and_replace(s: str, old: str, new: str) -> str:
    return s.replace(old, new)

# Find a trigger string and call a modify function on it
def find_and_modify(s: str, trigger: str, modify) -> str:
    start_pos = 0
    while (start_pos := s.find(trigger, start_pos)) != -1:
        start_pos = modify(s, start_pos)
    return s

def split_up(s: str):
    delims = "'\"`"
    find_ws = lambda ch: ch.isspace()
    s = s.strip()

    output = []
    embedded_quote = False
    key_char = ' '
    
    while s:
        if s[0] in delims:
            key_char = s[0]
            end = s.find(key_char, 1)
            while end != -1 and s[end - 1] == '\\':  # Handle escaped quotes
                end = s.find(key_char, end + 1)
                embedded_quote = True
            
            if end != -1:
                output.append(s[1:end])
                s = s[end + 1:]
            else:
                output.append(s[1:])
                s = ""
        else:
            it = next((i for i, ch in enumerate(s) if find_ws(ch)), len(s))
            output.append(s[:it])
            s = s[it:]
        
        # Transform any embedded quotes into the regular character
        if embedded_quote:
            output[-1] = output[-1].replace(f"\\{key_char}", key_char)
            embedded_quote = False
        
        s = s.strip()
    
    return output

def fix_newlines(leader: str, input_str: str) -> str:
    n = 0
    while n != -1 and n < len(input_str):
        n = input_str.find('\n', n)
        if n != -1:
            input_str = input_str[:n + 1] + leader + input_str[n + 1:]
            n += len(leader)
    return input_str

def escape_detect(s: str, offset: int) -> int:
    next_char = s[offset + 1]
    if next_char in {'"', "'", '`'}:
        astart = s.rfind("-/ \"'`", 0, offset)
        if astart != -1:
            if s[astart] == ('-' if s[offset] == '=' else '/'):
                s = s[:offset] + ' ' + s[offset + 1:]
    return offset + 1

def add_quotes_if_needed(s: str) -> str:
    if (s[0] != '"' and s[0] != "'") or s[0] != s[-1]:
        quote = "'" if s.find('"') < s.find("'") else '"'
        if ' ' in s:
            s = quote + s + quote
    return s

class ExitCodes(Enum):
    SUCCESS = 0
    INCORRECT_CONSTRUCTION = 100
    BAD_NAME_STRING = 101
    OPTION_ALREADY_ADDED = 102
    FILE_ERROR = 103
    CONVERSION_ERROR = 104
    VALIDATION_ERROR = 105
    REQUIRED_ERROR = 106
    REQUIRES_ERROR = 107
    EXCLUDES_ERROR = 108
    EXTRAS_ERROR = 109
    CONFIG_ERROR = 110
    INVALID_ERROR = 111
    HORRIBLE_ERROR = 112
    OPTION_NOT_FOUND = 113
    ARGUMENT_MISMATCH = 114
    BASE_CLASS = 127

# Base error class
class CLIError(Exception):
    def __init__(self, name, msg, exit_code=ExitCodes.BASE_CLASS):
        super().__init__(msg)
        self.name = name
        self.exit_code = exit_code

    def get_exit_code(self):
        return self.exit_code

    def get_name(self):
        return self.name

# Construction errors
class ConstructionError(CLIError):
    pass

class IncorrectConstruction(ConstructionError):
    def __init__(self, msg):
        super().__init__("IncorrectConstruction", msg, ExitCodes.INCORRECT_CONSTRUCTION)

class BadNameString(ConstructionError):
    def __init__(self, msg):
        super().__init__("BadNameString", msg, ExitCodes.BAD_NAME_STRING)

# Parsing errors
class ParseError(CLIError):
    pass

class FileError(ParseError):
    def __init__(self, msg):
        super().__init__("FileError", msg, ExitCodes.FILE_ERROR)

class ConversionError(ParseError):
    def __init__(self, msg):
        super().__init__("ConversionError", msg, ExitCodes.CONVERSION_ERROR)

class ValidationError(ParseError):
    def __init__(self, msg):
        super().__init__("ValidationError", msg, ExitCodes.VALIDATION_ERROR)

class RequiredError(ParseError):
    def __init__(self, msg):
        super().__init__("RequiredError", msg, ExitCodes.REQUIRED_ERROR)

class ArgumentMismatch(ParseError):
    def __init__(self, msg):
        super().__init__("ArgumentMismatch", msg, ExitCodes.ARGUMENT_MISMATCH)

# Utility functions
def split_up(string):
    output = []
    embedded_quote = False
    key_char = ''
    delimiters = {'\'', '"', '`'}
    while string:
        if string[0] in delimiters:
            key_char = string[0]
            end = string.find(key_char, 1)
            while end != -1 and string[end - 1] == '\\':
                end = string.find(key_char, end + 1)
                embedded_quote = True
            if end != -1:
                output.append(string[1:end])
                string = string[end + 1:].strip()
            else:
                output.append(string[1:])
                string = ''
        else:
            split_point = re.search(r'\s', string)
            if split_point:
                output.append(string[:split_point.start()])
                string = string[split_point.start():].strip()
            else:
                output.append(string)
                string = ''
        if embedded_quote:
            output[-1] = output[-1].replace(f'\\{key_char}', key_char)
            embedded_quote = False
    return output

def add_quotes_if_needed(string):
    if ' ' in string and not (string.startswith('"') or string.startswith("'")):
        quote = '"' if '"' not in string else "'"
        string = f"{quote}{string}{quote}"
    return string

from typing import Any, Union
import re

class CLI:
    
    # Type checking functions
    @staticmethod
    def is_vector(value: Any) -> bool:
        """Check if a value is a vector (list)"""
        return isinstance(value, list)

    @staticmethod
    def is_bool(value: Any) -> bool:
        """Check if a value is boolean"""
        return isinstance(value, bool)

    @staticmethod
    def type_name(value: Any) -> str:
        """Get the type name for a given value"""
        if isinstance(value, int) and value >= 0:
            return "UINT"
        elif isinstance(value, int):
            return "INT"
        elif isinstance(value, float):
            return "FLOAT"
        elif CLI.is_vector(value):
            return "VECTOR"
        else:
            return "TEXT"

    # Lexical cast
    @staticmethod
    def lexical_cast(input: str, output_type: type) -> Union[int, float, str, None]:
        """
        Attempt to cast a string input to the specified type.
        Returns the casted value if successful, or None if casting fails.
        """
        try:
            if output_type is int:
                # Check for signed integer
                if re.match(r"^-?\d+$", input):
                    return int(input)
            elif output_type is float:
                return float(input)
            elif output_type is str:
                return input
            elif CLI.is_vector(output_type):
                # Assume that vector means a list of strings
                return input.split(",")  # Split by comma for example
        except (ValueError, TypeError):
            return None  # Casting failed
        return None  # Unsupported type

    # Specialized casts for unsigned integers and floats
    @staticmethod
    def lexical_cast_unsigned(input: str) -> Union[int, None]:
        """Attempt to cast a string to an unsigned integer."""
        try:
            value = int(input)
            return value if value >= 0 else None
        except ValueError:
            return None

    @staticmethod
    def lexical_cast_float(input: str) -> Union[float, None]:
        """Attempt to cast a string to a floating-point number."""
        try:
            return float(input)
        except ValueError:
            return None

    # Utility function for testing purposes
    @staticmethod
    def parse_and_cast(input: str, output_type: type) -> Any:
        """
        Tries to cast the input string to the specified output_type.
        Returns the cast value or raises an error if it cannot be cast.
        """
        result = CLI.lexical_cast(input, output_type)
        if result is None:
            raise ValueError(f"Cannot cast '{input}' to {output_type.__name__}")
        return result


class CLI:
    class detail:

        @staticmethod
        def valid_first_char(char: str) -> bool:
            """Checks if the character is a valid starting character for an option name."""
            return re.match(r'[A-Za-z]', char) is not None

        @staticmethod
        def split_short(current: str) -> Tuple[bool, str, str]:
            """
            Splits a short option if valid.
            Returns (True, name, rest) if it is a valid short option, else (False, "", "")
            """
            if len(current) > 1 and current[0] == '-' and CLI.detail.valid_first_char(current[1]):
                name = current[1]
                rest = current[2:]
                return True, name, rest
            return False, "", ""

        @staticmethod
        def split_long(current: str) -> Tuple[bool, str, str]:
            """
            Splits a long option if valid.
            Returns (True, name, value) if it is a valid long option, else (False, "", "")
            """
            if len(current) > 2 and current.startswith("--") and CLI.detail.valid_first_char(current[2]):
                loc = current.find('=')
                if loc != -1:
                    name = current[2:loc]
                    value = current[loc + 1:]
                else:
                    name = current[2:]
                    value = ""
                return True, name, value
            return False, "", ""

        @staticmethod
        def split_windows(current: str) -> Tuple[bool, str, str]:
            """
            Splits a Windows-style option if valid.
            Returns (True, name, value) if it is a valid option, else (False, "", "")
            """
            if len(current) > 1 and current[0] == '/' and CLI.detail.valid_first_char(current[1]):
                loc = current.find(':')
                if loc != -1:
                    name = current[1:loc]
                    value = current[loc + 1:]
                else:
                    name = current[1:]
                    value = ""
                return True, name, value
            return False, "", ""

        @staticmethod
        def split_names(current: str) -> List[str]:
            """
            Splits a comma-separated string into a list of trimmed names.
            """
            return [name.strip() for name in current.split(',')]

        @staticmethod
        def get_names(input_list: List[str]) -> Tuple[List[str], List[str], str]:
            """
            Parses input list into short names, long names, and positional name.
            Returns a tuple of (short_names, long_names, pos_name).
            """
            short_names = []
            long_names = []
            pos_name = ""

            for name in input_list:
                if len(name) == 0:
                    continue
                elif len(name) > 1 and name[0] == '-' and name[1] != '-':
                    if len(name) == 2 and CLI.detail.valid_first_char(name[1]):
                        short_names.append(name[1])
                    else:
                        raise ValueError(f"One-character name expected in short option: '{name}'")
                elif len(name) > 2 and name.startswith("--"):
                    long_name = name[2:]
                    if CLI.detail.valid_name_string(long_name):
                        long_names.append(long_name)
                    else:
                        raise ValueError(f"Invalid long name: '{name}'")
                elif name in ("-", "--"):
                    raise ValueError(f"Dashes-only name not allowed: '{name}'")
                else:
                    if pos_name:
                        raise ValueError(f"Multiple positional names not allowed: '{name}'")
                    pos_name = name

            return short_names, long_names, pos_name

        @staticmethod
        def valid_name_string(name: str) -> bool:
            """Checks if a string is a valid long name."""
            return bool(re.match(r'^[A-Za-z][\w-]*$', name))



