import os
import time

import yaml
from loguru import logger

from rerwatcher.formatter import TransilienApiFormatter
from rerwatcher.api import TransilienApi
from rerwatcher.display import DisplayDeviceFactory


class RerWatcher:
    def __init__(self):
        logger.info("Building RERWatcher app...")
        config = RerWatcher.load_config()
        matrix_display = DisplayDeviceFactory.build(config)
        transilien_api = TransilienApi(config)
        transilien_formatter = TransilienApiFormatter()

        self._app = _App(
            config=config,
            display=matrix_display,
            api=transilien_api,
            formatter=transilien_formatter
        )
        logger.info("RERWatcher app built.")

    @staticmethod
    def load_config():
        with open('config.yml', 'r') as ymlconf:
            config = yaml.load(ymlconf, Loader=yaml.FullLoader)

        for section in config:
            for param in config[section]:
                env_key = f"{section}_{param}".upper()
                default_value = config[section][param]

                config[section][param] = os.environ.get(env_key, default_value)

        return config

    def start(self):
        logger.info("Starting RERWatcher app...")
        try:
            self._app.start()
        except KeyboardInterrupt:
            logger.info("RERWatcher app stopped.")
            pass


class _App:
    def __init__(self, config, display, api, formatter):
        self.is_running = False
        self.api = api
        self.display = display
        self.formatter = formatter
        self._refresh_time = config['refresh_time']['default']

    def start(self):
        self.is_running = True

        while self.is_running:
            response = self.api.fetch_data()
            timetables = self.formatter.format_response(response=response)
            self.display.print(timetables)
            self._manage_refresh_time()

    def _manage_refresh_time(self):
        time.sleep(self._refresh_time)
