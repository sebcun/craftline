from dataclasses import dataclass

import sys
if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    
@dataclass(frozen=True)
class Color:
    code: str
    
    def __call__(self, text: str) -> str:
        return f"{self.code}{text}{RESET.code}"

RESET = Color("\033[0m")

class FG:
    WHITE = Color("\033[97m")
    GRAY = Color("\033[90m")
    CYAN = Color("\033[96m")
    GREEN = Color("\033[92m")
    YELLOW = Color("\033[93m")
    RED = Color("\033[91m")
    BLUE = Color("\033[94m")
    MAGENTA = Color("\033[95m")

class Style:
    BOLD = Color("\033[1m")
    DIM = Color("\033[2m")

class Theme:
    TITLE = FG.CYAN
    ACCENT = FG.GREEN
    SELECTED = FG.WHITE
    MUTED = FG.GRAY
    WARNING = FG.YELLOW
    ERROR = FG.RED
    INFO = FG.BLUE