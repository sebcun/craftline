import os
from pathlib import Path

def get_app_data_dir() -> Path:
    return Path(os.environ["APPDATA"]) / "Craftline"

def get_directories() -> dict[str, Path]:
    root = get_app_data_dir()
    return {
        "root": root,
        "instances": root / "instances",
        "auth": root / "auth",
        "cache": root / "cache",
        "runtimes": root / "runtimes",
        "logs": root / "logs"
    }