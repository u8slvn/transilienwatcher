#!/usr/bin/env python3
# coding: utf-8

import app


try:
    rer_watcher = app.build_rer_watcher()
    rer_watcher.start()
except KeyboardInterrupt:
    pass
