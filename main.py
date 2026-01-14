import sys

from src.craftline.logging_setup import setup_logging
from src.craftline.bootstrap import bootstrap


def main() -> int:
    setup_logging()
    
    if not bootstrap():
        return 1
    
    print("Craftline loaded.")
    return 0

if __name__== "__main__":
    sys.exit(main())