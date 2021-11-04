#!/usr/bin/env python3
# coding: utf-8
import argparse
from pathlib import Path

from loguru import logger

from transilienwatcher import TransilienWatcher


parser = argparse.ArgumentParser(description="TransilienWatcher")
parser.add_argument(
    dest="operation",
    type=str,
    choices=["start", "stop", "status"],
    help="TransilienWatcher commands.",
)
parser.add_argument(
    "-c",
    "--config",
    dest="config_file",
    action="store",
    help="TransilienWatcher configuration file.",
)
parser.add_argument(
    "-l",
    "--log",
    dest="log_file",
    action="store",
    help="TransilienWatcher log file.",
)
args = parser.parse_args()


config_file = args.config_file or "config.yml"
log_file = args.config_file or f"{Path.home()}/transilenwatcher.log"

logger.remove()  # Reset default loguru logger.
logger.add(log_file, rotation="00:00", retention="2 days", level="DEBUG")

daemon = TransilienWatcher(log_file=log_file, config_file=config_file)
operation = getattr(daemon, args.operation)
operation()
