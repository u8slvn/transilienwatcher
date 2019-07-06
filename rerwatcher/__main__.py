#!/usr/bin/env python3
# coding: utf-8
from loguru import logger

from . import build_rer_watcher

logger.add("log/file_{time}.log", rotation="12:00")

# RERWatcher entrypoint.
try:
    logger.info("Building RERWatcher app...")
    rer_watcher = build_rer_watcher()
    logger.info("RERWatcher app built.")
    logger.info("Starting RERWatcher app...")
    rer_watcher.start()
except KeyboardInterrupt:
    logger.info("RERWatcher app stopped.")
    pass
