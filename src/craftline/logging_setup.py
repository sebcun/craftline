import logging
import sys
from datetime import datetime
from pathlib import Path

from src.craftline.paths import get_directories

def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    handlers: list[logging.Handler] = [console_handler]
    
    logs_dir = get_directories()["logs"]
    if logs_dir.exists():
        log_file = logs_dir / f"craftline_{datetime.now():%Y%m%d_%H%M%S}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
        
    logging.basicConfig(level=level, handlers=handlers)