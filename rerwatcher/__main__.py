#!/usr/bin/env python3
# coding: utf-8
from loguru import logger

from rerwatcher.app import RerWatcher

logger.add("log/file_{time}.log", rotation="00:00", retention="2 days")

rer_watcher = RerWatcher()
rer_watcher.start()
