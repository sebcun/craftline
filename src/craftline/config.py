import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from src.craftline.paths import get_app_data_dir

logger = logging.getLogger(__name__)

CURRENT_CONFIG_VERSION = 1

@dataclass
class AppConfig:
    first_run_complete: bool = False
    check_updates: bool = True
    theme: str = "auto"

@dataclass
class InstancesConfig:
    default_instance: str | None = None
    last_played: str | None = None
    
@dataclass
class AuthConfig:
    active_account: str | None = None
    
@dataclass
class JavaConfig:
    prefer_bundled: bool = True
    custom_path: str | None = None
    
@dataclass
class LauncherConfig:
    close_on_launch: bool = False
    default_memory_mb: int = 2048
    max_memory_mb: int = 8192
    
@dataclass
class CraftlineConfig:
    config_version: int = CURRENT_CONFIG_VERSION
    app: AppConfig = field(default_factory=AppConfig)
    instances: InstancesConfig = field(default_factory=InstancesConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    java: JavaConfig = field(default_factory=JavaConfig)
    launcher: LauncherConfig = field(default_factory=LauncherConfig)

def get_config_path() -> Path:
    return get_app_data_dir() / "craftline.json"

def _dict_to_config(data: dict[str, Any]) -> CraftlineConfig:
    return CraftlineConfig(
        config_version=data.get("config_version", CURRENT_CONFIG_VERSION),
        app=AppConfig(**{
            k: v for k, v in data.get("app", {}).items()
            if k in AppConfig.__dataclass_fields__
        }),
        instances=InstancesConfig(**{
            k: v for k, v in data.get("instances", {}).items()
            if k in InstancesConfig.__dataclass_fields__
        }),
        auth=AuthConfig(**{
            k: v for k, v in data.get("auth", {}).items()
            if k in AuthConfig.__dataclass_fields__
        }),
        java=JavaConfig(**{
            k: v for k, v in data.get("java", {}).items()
            if k in JavaConfig.__dataclass_fields__
        }),
        launcher=LauncherConfig(**{
            k: v for k, v in data.get("launcher", {}).items()
            if k in LauncherConfig.__dataclass_fields__
        }),
    )
    
def _config_to_dict(config: CraftlineConfig) -> dict[str, Any]:
    return {
        "config_version": config.config_version,
        "app": asdict(config.app),
        "instances": asdict(config.instances),
        "auth": asdict(config.auth),
        "java": asdict(config.java),
        "launcher": asdict(config.launcher)
    }
    
def _migrate_config(data: dict[str, Any]) -> dict[str, Any]:
    version = data.get("config_version", 0)
    
    if version == 0:
        logger.info("Migrating config from legacy to v1")
        new_data = _config_to_dict(CraftlineConfig())
        
        if "first_run_complete" in data:
            new_data["app"]["first_run_complete"] = data["first_run_complete"]
            data = new_data
            version = 1
            
    data["config_version"] = version
    logger.info("Migration of config successful")
    
def validate_config(config: CraftlineConfig) -> list[str]:
    warnings: list[str] = []
    
    if config.launcher.default_memory_mb < 512:
        warnings.append("default_memory_mb below 512MB may cause issues")
        
    if config.launcher.max_memory_mb < config.launcher.default_memory_mb:
        warnings.append("max_memory_mb is less than default_memory_mb")
        
    if config.app.theme not in ("auto", "light", "dark"):
        warnings.append(f"Unknown theme '{config.app.theme}', defaulting to auto")
        
    return warnings
    
def load_config() -> CraftlineConfig:
    config_path = get_config_path()
    
    if not config_path.exists():
        logger.debug("No config file found, using defaults")
        return CraftlineConfig()
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.warning(f"Config file corrupted, using defaults: {e}")
        return CraftlineConfig()
    except OSError as e:
        logger.warning(f"Failed to read config file, using defaults: {e}")
        return CraftlineConfig()
    
    if data.get("config_version", 0) < CURRENT_CONFIG_VERSION:
        data = _migrate_config(data)
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved migrated config")
        except OSError as e:
            logger.warning(f"Failed to save migrated config: {e}")
    
    config = _dict_to_config(data)
    
    for warning in validate_config(config):
        logger.warning(f"Config validation: {warning}")
    
    return config       
    
def save_config(config: CraftlineConfig) -> bool:
    config_path = get_config_path()
    
    try:
        data = _config_to_dict(config)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.debug("Config saved successfully")
        return True
    except OSError as e:
        logger.error(f"Failed to save config: {e}")
        return False

def get_default_config() -> CraftlineConfig:
    return CraftlineConfig()