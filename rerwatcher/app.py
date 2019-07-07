import os
import time

import yaml
from loguru import logger

from rerwatcher.api import TransilienApi
from rerwatcher.daemon import Daemon
from rerwatcher.display import DisplayDeviceFactory
from rerwatcher.formatter import TransilienApiFormatter


class RerWatcher(Daemon):
    def __init__(self, *args, **kwargs):
        app_name = self.__class__.__name__
        super(RerWatcher, self).__init__(app_name=app_name, *args, **kwargs)

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

    def run(self):
        logger.info("Starting RERWatcher app...")
        self._app.start()


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
            self.display.print(messages=timetables)
            self._manage_refresh_time()

    def _manage_refresh_time(self):
        time.sleep(self._refresh_time)
