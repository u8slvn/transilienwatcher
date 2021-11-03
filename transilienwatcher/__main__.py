#!/usr/bin/env python3
# coding: utf-8
import argparse
from pathlib import Path

from loguru import logger

from transilienwatcher import TransilienWatcher

log_file = f"{Path.home()}/transilenwatcher.log"

logger.remove()  # Reset default loguru logger.
logger.add(log_file, rotation="00:00", retention="2 days", level="DEBUG")


def parse_operation():
    choices = ["start", "stop", "status"]
    parser = argparse.ArgumentParser(description="TransilienWatcher")
    parser.add_argument("operation", type=str, choices=choices)
    args = parser.parse_args()
    return args.operation


daemon = TransilienWatcher(log_file=log_file)

operation = parse_operation()
operation = getattr(daemon, operation)
operation()
