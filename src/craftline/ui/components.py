from dataclasses import dataclass, field
from typing import Callable, Optional, Any

from src.craftline.ui.colors import Theme, FG
from src.craftline.ui.input import read_key, Key, KeyEvent
from src.craftline.ui.screen import Screen

@dataclass
class MenuItem:
    label: str
    action: Optional[Callable[[], Any]] = None
    disabled: bool = False
    
@dataclass
class Menu:
    items: list[MenuItem] =  field(default_factory=list)
    selected: int = 0
    
    
    def render(self) -> list[str]:
        lines = []
        
        for i, item in enumerate(self.items):
            
            if i == self.selected:
                prefix = Theme.ACCENT(">")
                label = Theme.SELECTED(item.label)
                
            elif item.disabled:
                prefix = " "
                label = Theme.MUTED(item.label)
                
            else:
                prefix = " "
                label = item.label
        
            lines.append(f" {prefix} {label}")
            
        return lines
    
    
    def handle_input(self, event: KeyEvent) -> Optional[Any]:
        if event.key == Key.UP:
            self._move(-1)
        
        elif event.key == Key.DOWN:
            self._move(1)
            
        elif event.key == Key.ENTER:
            item = self.items[self.selected]
            if not item.disabled and item.action:
                return item.action()
        return None
    
    def _move(self, direction: int) -> None:
        new_pos = self.selected
        
        for _ in range(len(self.items)):
            
            new_pos = (new_pos + direction) % len(self.items)
            
            if not self.items[new_pos].disabled:
                self.selected = new_pos
                break
            
@dataclass
class MessageBox:
    title: str
    message: str
    style: str = "info"
    
    def render(self) -> list[str]:
        
        color = {
            "info": Theme.INFO,
            "warning": Theme.WARNING,
            "error": Theme.ERROR
        }.get(self.style, Theme.INFO)
        
        lines = [
            "",
            f"  {color(self.title)}",
            "",
            f"  {self.message}",
            "",
        ]
        return lines