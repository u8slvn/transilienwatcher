#!/usr/bin/env python3
# coding: utf-8

import os
import time

import yaml

from rerwatcher.display import DisplayDeviceFactory
from rerwatcher.api import TransilienApi


def load_config():
    """Load RerWatcher configuration

    Load the default configuration from 'config.yml' file and check for
    each parameters from each sections if no environment variables is
    set. If it does, the default yaml value is overwrite by the
    environment's one.
    """
    with open('config.yml', 'r') as ymlconf:
        config = yaml.load(ymlconf)

    for section in config:
        for param in config[section]:
            env_key = "{section}_{param}".format(
                section=section,
                param=param,
            ).upper()
            default_value = config[section][param]

            config[section][param] = os.environ.get(env_key, default_value)

    return config


def build_rer_watcher():
    config = load_config()

    matrix_display = DisplayDeviceFactory.build(config)

    app = RerWatcher(
        config=config,
        display=matrix_display
    )

    return app


class RerWatcher:
    def __init__(self, config, display):
        self.is_running = False
        self._api = TransilienApi(config)
        self._display = display
        self._refresh_time = config.getint('refresh_time', 'default')
        self._refresh_time_step = config.getint('refresh_time', 'step')
        self._refresh_time_max = config.getint('refresh_time', 'max')

    def start(self):
        self.is_running = True

        while self.is_running:
            timetables = self._api.fetch_data()
            self._display.print(timetables)
            self._manage_refresh_time()

    def _manage_refresh_time(self):
        time.sleep(self._refresh_time)

    def _increase_refresh_time(self):
        if self._refresh_time < self._refresh_time_max:
            self._refresh_time += self._refresh_time_step
