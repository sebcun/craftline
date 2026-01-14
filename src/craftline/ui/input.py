import msvcrt
from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass

class Key(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()
    ESCAPE = auto()
    BACKSPACE = auto()
    TAB = auto()
    CHAR = auto()
    
@dataclass
class KeyEvent:
    key: Key
    char: Optional[str] = None
    
def read_key() -> KeyEvent:
    ch = msvcrt.getwch()
    
    if ch in ('\x00', '\xe0'):
        ext = msvcrt.getwch()
        mapping = {
            'H': Key.UP,
            'P': Key.DOWN,
            'K': Key.LEFT,
            'M': Key.RIGHT
        }
        return KeyEvent(mapping.get(ext, Key.CHAR), None)

    if ch == '\r':
        return KeyEvent(Key.ENTER)
    if ch == '\x1b':
        return KeyEvent(Key.ESCAPE)
    if ch == '\x08':
        return KeyEvent(Key.BACKSPACE)
    if ch == '\t':
        return KeyEvent(Key.TAB)
    
    return KeyEvent(Key.CHAR, ch)