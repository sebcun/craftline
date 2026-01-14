import sys
from typing import Optional

from src.craftline.ui.screen import Screen
from src.craftline.ui.components import Menu, MenuItem
from src.craftline.ui.input import read_key, Key
from src.craftline.ui.colors import Theme

class MainMenuScreen:
    def __init__(self, username: Optional[str] = None):
        self.username = username
        self.running = True
        self.screen = Screen(
            title="Main Menu",
            footer_hint="↑↓ Navigate  Enter Select  Esc Quit"
        )
        self.menu = Menu(items=[
            MenuItem("Play", action=self._play),
            MenuItem("Instances", action=self._instances),
            MenuItem("Settings", action=self._settings),
            MenuItem("Exit", action=self._exit),
        ])
        
    def _get_user_display(self) -> str:
        if self.username:
            return Theme.ACCENT(self.username)
        return Theme.MUTED("Not logged in")
    
    def _play(self) -> None:
        pass

    def _instances(self) -> None:
        pass

    def _settings(self) -> None:
        pass

    def _exit(self) -> None:
        self.running = False

    def render(self) -> None:
        inner = self.screen.width - 2
        user_display = self._get_user_display()
        user_len = self.screen._visible_len(user_display)
        
        content = []
        content.append(" " * (inner - user_len - 2) + user_display)
        content.append("")
        content.extend(self.menu.render())
        content.append("")
        
        self.screen.render(content)

    def run(self) -> int:
        while self.running:
            self.render()
            event = read_key()
            
            if event.key == Key.ESCAPE:
                self.running = False
            else:
                self.menu.handle_input(event)
        
        return 0