#!/usr/bin/env python3
# coding: utf-8

import os
import time

import requests
import yaml

from rerwatcher.display_device import DisplayDeviceFactory
from requests.auth import HTTPBasicAuth
from rerwatcher.transilien_api import TransilienApiDriver


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

    api_driver = TransilienApiDriver(config)

    matrix_device = DisplayDeviceFactory.build(config)

    app = RerWatcher(
        config=config,
        api_driver=api_driver,
        display_device=matrix_device
    )

    return app


class RerWatcher:
    def __init__(self, config, api_driver, display_device):
        self.is_running = False
        self._api_url = config.get('api', 'url')
        self._api_auth = HTTPBasicAuth(
            username=config.get('api', 'user'),
            password=config.get('api', 'password')
        )
        self._refresh_time = config.getint('refresh_time', 'default')
        self._refresh_time_step = config.getint('refresh_time', 'step')
        self._refresh_time_max = config.getint('refresh_time', 'max')
        self.api_driver = api_driver
        self._display_device = display_device

    def start(self):
        self.is_running = True

        # TODO - manage context error
        while self.is_running:
            response = self._fetch_api()
            # TODO - check status_code == 200
            timetables = self.api_driver.get_timetables(response=response)
            self._display_timetables(timetables=timetables)
            self._manage_refresh_time()

    def _fetch_api(self):
        return requests.get(url=self._api_url, auth=self._api_auth)

    def _display_timetables(self, timetables):
        self._display_device.print(timetables)

    def _manage_refresh_time(self):
        time.sleep(self._refresh_time)

    def _increase_refresh_time(self):
        if self._refresh_time < self._refresh_time_max:
            self._refresh_time += self._refresh_time_step
