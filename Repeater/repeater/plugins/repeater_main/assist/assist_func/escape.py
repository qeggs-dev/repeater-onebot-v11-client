from typing import Callable

ESCAPE_CHARACTERS: dict[str, str | Callable[[str], str]] = {
    "0": "\0",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "\\": "\\",
    "\"": "\"",
    "\'": "\'",
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "v": "\v",
    "e": "\x1b",
    "x": lambda x: chr(int(x, 16)),
    "u": lambda x: chr(int(x, 16)),
    "U": lambda x: chr(int(x, 16)),
    "o": lambda x: chr(int(x, 8)),
    "d": lambda x: chr(int(x, 10)),
}

INT_CHARACTERS: set[str] = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
}

OCTAL_CHARACTERS: set[str] = {
    "0", "1", "2", "3", "4", "5", "6", "7"
}

HEX_CHARACTERS: set[str] = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "a", "b", "c", "d", "e", "f",
    "A", "B", "C", "D", "E", "F"
}

def _find_continuous_digits(string: str, start: int, valid_digits: set) -> str:
    """
    Find continuous digits of the specified base
    """
    output = ""
    for char in string[start:]:
        if char in valid_digits:
            output += char
        else:
            break
    return output

def escape_string(string: str) -> str:
    """
    Process escape sequences in a string
    """
    output = ""
    i = 0
    length = len(string)
    
    while i < length:
        char = string[i]
        if char == "\\":
            if i + 1 >= length:
                raise ValueError("Invalid escape sequence at end of string")
            
            next_char = string[i + 1]
            if next_char in ESCAPE_CHARACTERS:
                escape = ESCAPE_CHARACTERS[next_char]
                if isinstance(escape, str):
                    # Special handling for \0 followed by octal digits
                    if next_char == "0":
                        # Check if there are more octal digits following
                        digits = _find_continuous_digits(string, i + 2, OCTAL_CHARACTERS)
                        if digits:
                            # Combine \0 with the following octal digits
                            full_octal = "0" + digits
                            output += chr(int(full_octal, 8))
                            i += 2 + len(digits)
                            continue
                    output += escape
                    i += 2
                else:
                    # Handle numeric escapes (x, u, U, o, d)
                    if next_char in ("x", "u", "U"):
                        # Hex sequences
                        digits = _find_continuous_digits(string, i + 2, HEX_CHARACTERS)
                        if not digits:
                            raise ValueError(f"Invalid \\{next_char} escape sequence at position {i}")
                        if next_char == "x" and len(digits) != 2:
                            raise ValueError("\\x escape sequence requires exactly 2 hex digits")
                        elif next_char == "u" and len(digits) != 4:
                            raise ValueError("\\u escape sequence requires exactly 4 hex digits")
                        elif next_char == "U" and len(digits) != 8:
                            raise ValueError("\\U escape sequence requires exactly 8 hex digits")
                        output += escape(digits)
                        i += 2 + len(digits)
                    elif next_char == "o":
                        # Octal sequence
                        digits = _find_continuous_digits(string, i + 2, OCTAL_CHARACTERS)
                        if not digits:
                            raise ValueError(f"Invalid \\o escape sequence at position {i}")
                        output += escape(digits)
                        i += 2 + len(digits)
                    elif next_char == "d":
                        # Decimal sequence
                        digits = _find_continuous_digits(string, i + 2, INT_CHARACTERS)
                        if not digits:
                            raise ValueError(f"Invalid \\d escape sequence at position {i}")
                        output += escape(digits)
                        i += 2 + len(digits)
            else:
                # Check for octal escape sequence starting with a digit (0-7)
                if next_char in OCTAL_CHARACTERS:
                    digits = _find_continuous_digits(string, i + 1, OCTAL_CHARACTERS)
                    if digits:
                        output += chr(int(digits, 8))
                        i += 1 + len(digits)
                    else:
                        raise ValueError(f"Invalid octal escape sequence at position {i}")
                else:
                    raise ValueError(f"Invalid escape character: '\\{next_char}' at position {i}")
        else:
            output += char
            i += 1
    
    return output