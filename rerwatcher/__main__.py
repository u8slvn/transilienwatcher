#!/usr/bin/env python3
# coding: utf-8

from app import build_rer_watcher


try:
    rer_watcher = build_rer_watcher()
    rer_watcher.start()
except KeyboardInterrupt:
    pass
