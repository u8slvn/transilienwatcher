#!/usr/bin/env python3
# coding: utf-8
import os
import time

import yaml
from loguru import logger

from rerwatcher.api import TransilienApi
from rerwatcher.display import DisplayDeviceFactory


class RerWatcher:
    def __init__(self):
        logger.info("Building RERWatcher app...")
        config = RerWatcher.load_config()
        matrix_display = DisplayDeviceFactory.build(config)
        transilien_api = TransilienApi(config)

        self._app = _App(
            config=config,
            display=matrix_display,
            api=transilien_api
        )
        logger.info("RERWatcher app built.")

    @staticmethod
    def load_config():
        """Load RerWatcher configuration

        Load the default configuration from 'config.yml' file and check for
        each parameters from each sections if no environment variables is
        set. If it does, the default yaml value is overwrite by the
        environment's one.

        Returns:
            config (dict): the global rerwatcher configuration

        """
        with open('config.yml', 'r') as ymlconf:
            config = yaml.load(ymlconf, Loader=yaml.FullLoader)

        for section in config:
            for param in config[section]:
                env_key = "{section}_{param}".format(
                    section=section,
                    param=param,
                ).upper()
                default_value = config[section][param]

                config[section][param] = os.environ.get(env_key,
                                                        default_value)

        return config

    def start(self):
        logger.info("Starting RERWatcher app...")
        try:
            self._app.start()
        except KeyboardInterrupt:
            logger.info("RERWatcher app stopped.")
            pass


class _App:
    def __init__(self, config, display, api):
        self.is_running = False
        self._api = api
        self._display = display
        self._refresh_time = config['refresh_time']['default']

    def start(self):
        self.is_running = True

        while self.is_running:
            timetables = self._api.fetch_data()
            self._display.print(timetables)
            self._manage_refresh_time()

    def _manage_refresh_time(self):
        time.sleep(self._refresh_time)
