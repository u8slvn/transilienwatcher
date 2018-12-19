#!/usr/bin/env python3
# coding: utf-8

from . import build_rer_watcher

# RERWatcher entrypoint.
try:
    rer_watcher = build_rer_watcher()
    rer_watcher.start()
except KeyboardInterrupt:
    pass
