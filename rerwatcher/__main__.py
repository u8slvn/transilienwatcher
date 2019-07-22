#!/usr/bin/env python3
# coding: utf-8
import argparse
import os

from loguru import logger

from rerwatcher import RerWatcher

log_success = f'{os.path.dirname(__file__)}/../log/rerwatcher.success.log'
log_error = f'{os.path.dirname(__file__)}/../log/rerwatcher.error.log'

logger.remove()  # Reset default loguru logger.
logger.add(log_success, rotation='00:00', retention='2 days', level='DEBUG')
logger.add(log_error, rotation='00:00', retention='2 days', level='ERROR')


def parse_operation():
    choices = ['start', 'stop', 'status']
    parser = argparse.ArgumentParser(description="RERWatcher")
    parser.add_argument('operation', type=str, choices=choices)
    args = parser.parse_args()
    return args.operation


daemon = RerWatcher(
    pidfile='/tmp/rerwatcher.pid',
    stdout=log_success,
    stderr=log_error
)

operation = parse_operation()
operation = getattr(daemon, operation)
operation()
