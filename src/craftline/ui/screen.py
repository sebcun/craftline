import os
import shutil
from dataclasses import dataclass, field
from typing import Callable, Optional

from src.craftline import __version__, __app_name__
from src.craftline.ui.colors import Theme, FG, Style, RESET


@dataclass
class Screen:
    title: str = ""
    subtitle: str = ""
    footer_hint: str = "↑↓ Navigate  Enter Select  Esc Back"
    width: int = field(default_factory=lambda: shutil.get_terminal_size().columns)

    BOX_H = "─"
    BOX_V = "│"
    BOX_TL = "┌"
    BOX_TR = "┐"
    BOX_BL = "└"
    BOX_BR = "┘"
    BOX_ML = "├"
    BOX_MR = "┤"

    def clear(self) -> None:
        os.system("cls")

    def _line(self, left: str, fill: str, right: str, content: str = "") -> str:
        inner_width = self.width - 2
        if content:
            padding = inner_width - self._visible_len(content)
            return f"{left}{content}{' ' * padding}{right}"
        return f"{left}{fill * inner_width}{right}"

    def _visible_len(self, text: str) -> int:
        import re

        return len(re.sub(r"\033\[[0-9;]*m", "", text))

    def _center(self, text: str, width: int) -> str:
        visible = self._visible_len(text)
        padding = (width - visible) // 2
        return " " * padding + text + " " * (width - padding - visible)

    def render_header(self) -> list[str]:
        lines = []
        inner = self.width - 2

        app_title = f" {__app_name__} v{__version__}"
        border_left = self.BOX_TL + self.BOX_H * 2
        border_right = self.BOX_H * (inner - len(app_title) - 2) + self.BOX_TR
        lines.append(
            Theme.MUTED(border_left)
            + Theme.TITLE(app_title)
            + Theme.MUTED(border_right)
        )

        if self.title:
            title_text = f" {Theme.ACCENT(self.title)}"
            lines.append(
                Theme.MUTED(self.BOX_V)
                + title_text
                + " " * (inner - self._visible_len(title_text))
                + Theme.MUTED(self.BOX_V)
            )

        if self.subtitle:
            sub_text = f" {Theme.MUTED(self.subtitle)}"
            lines.append(
                Theme.MUTED(self.BOX_V)
                + sub_text
                + " " * (inner - self._visible_len(sub_text))
                + Theme.MUTED(self.BOX_V)
            )

        lines.append(Theme.MUTED(self._line(self.BOX_ML, self.BOX_H, self.BOX_MR)))

        return lines

    def render_footer(self) -> list[str]:
        lines = []
        inner = self.width - 2

        lines.append(Theme.MUTED(self._line(self.BOX_ML, self.BOX_H, self.BOX_MR)))
        
        hint = self._center(Theme.MUTED(self.footer_hint), inner)
        lines.append(Theme.MUTED(self.BOX_V) + hint + Theme.MUTED(self.BOX_V))
        
        lines.append(Theme.MUTED(self._line(self.BOX_BL, self.BOX_H, self.BOX_BR)))
        
        return lines
    
    def render_content_line(self, text: str = "") -> str:
        inner = self.width - 2
        content = f" {text}" if text else ""
        padding = inner - self._visible_len(content)
        return Theme.MUTED(self.BOX_V) + content + " " * padding + Theme.MUTED(self.BOX_V)
    
    def render(self, content_lines: list[str]) -> None:
        self.clear()
        
        for line in self.render_header():
            print(line)
            
        for line in content_lines:
            print(self.render_content_line(line))
            
        for line in self.render_footer():
            print(line)
