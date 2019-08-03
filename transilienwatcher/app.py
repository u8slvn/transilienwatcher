import os
import tempfile
import time

from loguru import logger

from transilienwatcher.configuration import ConfigLoader
from transilienwatcher.daemon import Daemon
from transilienwatcher.display import DisplayBuilder
from transilienwatcher.transilien import Transilien


class TransilienWatcher(Daemon):
    def __init__(self, log_file: str):
        pidfile = os.path.join(tempfile.gettempdir(), 'transilienwatcher.pid')
        app_name = self.__class__.__name__
        super().__init__(
            pidfile=pidfile,
            app_name=app_name,
            stderr=log_file,
            stdout=log_file
        )

        config = ConfigLoader.load()
        display = DisplayBuilder.build(config['display'])
        transilien = Transilien(config['transilien'])

        self._app = _App(
            config=config,
            display=display,
            transilien=transilien,
        )

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
