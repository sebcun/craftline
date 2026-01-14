import sys

from src.craftline.logging_setup import setup_logging
from src.craftline.bootstrap import bootstrap

from src.craftline.ui.screens.main_menu import MainMenuScreen


def main() -> int:
    setup_logging()
    
    if not bootstrap():
        return 1
    
    username = None
    
    screen = MainMenuScreen(username=username)

    return screen.run()

if __name__== "__main__":
    sys.exit(main())