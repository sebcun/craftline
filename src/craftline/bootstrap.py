import logging

from src.craftline.paths import get_directories
from src.craftline.config import load_config, save_config

logger = logging.getLogger(__name__)

def ensure_directories() -> bool:
    directories = get_directories()
    
    for name, path in directories.items():
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {path}")
        except OSError as e:
            logger.error(f"Failed to create {name} directory at {path}: {e}")
            return False
    
    return True

def bootstrap() -> bool:
    logger.info("Starting Craftline bootstrap...")
    
    if not ensure_directories():
        logger.error("Bootstrap failed: could not create directories")
        return False
    
    from src.craftline.logging_setup import setup_logging
    setup_logging()
    
    config = load_config()
    
    if not config.app.first_run_complete:
        logger.info("First run detected, initializing defaults...")
        config.app.first_run_complete = True
        
        if not save_config(config):
            logger.error("Bootstrap failed: could not save config")
            return False
    
    logger.info("Bootstrap complete")
    return True