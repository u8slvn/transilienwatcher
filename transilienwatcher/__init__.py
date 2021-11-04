from pathlib import Path

from transilienwatcher.app import TransilienWatcher
from transilienwatcher.configuration import ConfigManager

WORKSPACE = f"{Path.home()}/transilenwatcher"
CONFIG_FILE = f"{WORKSPACE}/config.yml"
LOG_FILE = f"{WORKSPACE}/transilenwatcher.log"

__all__ = [
    "TransilienWatcher",
    "ConfigManager",
    "WORKSPACE",
    "CONFIG_FILE",
    "LOG_FILE",
]
