#!/usr/bin/env python3
# coding: utf-8

import time


class RerWatcher:
    def __init__(self, config, display, api):
        self.is_running = False
        self._api = api
        self._display = display
        self._refresh_time = config['refresh_time']['default']
        self._refresh_time_step = config['refresh_time']['step']
        self._refresh_time_max = config['refresh_time']['max']

    def start(self):
        self.is_running = True

        while self.is_running:
            timetables = self._api.fetch_data()
            self._display.print(timetables)
            self._manage_refresh_time()

    def _manage_refresh_time(self):
        time.sleep(self._refresh_time)
