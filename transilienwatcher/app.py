import time

import yaml
from loguru import logger

from transilienwatcher.transilien import Transilien
from transilienwatcher.daemon import Daemon
from transilienwatcher.display import DisplayBuilder
from transilienwatcher.utils import overwrite_config_with_env


class TransilienWatcher(Daemon):
    def __init__(self, *args, **kwargs):
        app_name = self.__class__.__name__
        super().__init__(app_name=app_name, *args, **kwargs)

        config = TransilienWatcher.load_config()
        display = DisplayBuilder.build(config['display'])
        transilien = Transilien(config['transilien'])

        self._app = _App(
            config=config,
            display=display,
            transilien=transilien,
        )

    @staticmethod
    def load_config():
        with open('config.yml', 'r') as ymlconf:
            config = yaml.load(ymlconf, Loader=yaml.FullLoader)
        config = overwrite_config_with_env(config)
        return config

    def run(self):
        logger.info("Starting RERWatcher app...")
        self._app.start()


class _App:
    def __init__(self, config, display, transilien):
        self.is_running = False
        self.transilien = transilien
        self.display = display
        self._refresh_time = config['refresh_time']

    def start(self):
        self.is_running = True

        while self.is_running:
            messages = self.transilien.fetch_data()
            self.display.print(messages=messages)
            self._manage_refresh_time()

    def _manage_refresh_time(self):
        time.sleep(self._refresh_time)
