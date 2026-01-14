import json
import logging
from pathlib import Path
from typing import Any

from src.craftline.paths import get_app_data_dir

logger = logging.getLogger(__name__)

DEFAULT_CONFIG: dict[str, Any] = {
    "version": "0.1.0",
    "first_run_complete": False,
}

def get_config_path() -> Path:
    return get_app_data_dir() / "craftline.json"

def load_config() -> dict[str, Any]:
    config_path = get_config_path()
    
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Failed to load config, using defaults: {e}")
        return DEFAULT_CONFIG.copy()
    
def save_config(config: dict[str, Any]) -> bool:
    config_path = get_config_path()
    
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        return True
    except OSError as e:
        logger.error(f"Failed to save config: {e}")
        return False