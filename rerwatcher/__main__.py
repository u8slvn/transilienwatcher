#!/usr/bin/env python3
# coding: utf-8
import os
import sys

from loguru import logger

from rerwatcher import RerWatcher

log_success = f'{os.path.dirname(__file__)}/../log/rerwatcher.success.log'
log_error = f'{os.path.dirname(__file__)}/../log/rerwatcher.error.log'

logger.remove()  # Reset default loguru logger.
logger.add(log_success, rotation='00:00', retention='2 days', level='DEBUG')
logger.add(log_error, rotation='00:00', retention='2 days', level='ERROR')

daemon = RerWatcher(
    pidfile='/tmp/rerwatcher.pid',
    stdout=log_success,
    stderr=log_error
)

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [start|stop].", file=sys.stderr)
    raise SystemExit(1)

if 'start' == sys.argv[1]:
    daemon.start()
elif 'stop' == sys.argv[1]:
    daemon.stop()
else:
    print(f"Unknown command {sys.argv[1]!r}.", file=sys.stderr)
    raise SystemExit(1)
