#!/usr/bin/env python3
# coding: utf-8

import time
from configparser import RawConfigParser
from datetime import datetime

import requests
# from luma.core.interface.serial import spi, noop
# from luma.core.legacy import text
# from luma.core.legacy.font import proportional, LCD_FONT
# from luma.core.render import canvas
# from luma.led_matrix.device import max7219
from lxml import etree
from requests.auth import HTTPBasicAuth


def timedelta_formatter(time_value):
    hours = time_value.seconds // 3600
    minutes = (time_value.seconds // 60) % 60
    if minutes < 1:
        minutes = 1

    str = "{}min".format(minutes)
    if hours > 1:
        str = "{}h".format(hours)

    return str


def matrix_device_builder():
    # serial = spi(port=0, device=0, gpio=noop())
    # device = max7219(serial, width=64, height=16, block_orientation=-90, rotate=0)
    # return device.contrast(32)
    return True


def bootstrap():
    config = RawConfigParser()
    config.read('settings.ini')

    matrix_device = matrix_device_builder()

    app = RERWatcher(
        config=config,
        display_device=matrix_device
    )
    app.start()


class RERWatcher:
    def __init__(self, config, display_device):
        self.is_running = False
        self._config = config
        self._api_date_format = self._config.get('API', 'DateFormat')
        self._refresh_time = self._config.getint('REFRESH_TIME', 'Default')
        self._step_refresh_time = self._config.getint('REFRESH_TIME', 'Step')
        self._max_refresh_time = self._config.getint('REFRESH_TIME', 'Max')
        self._display_device = display_device

    def start(self):
        self.is_running = True

        while self.is_running:
            api_result = self.fetch_api()
            timetables = self.extract_timetables(api_load=api_result)
            self.display_timetables(timetables=timetables)
            self.manage_refresh_time()

    def fetch_api(self):
        return requests.get(
            url=self._config.get('API', 'Url'),
            auth=HTTPBasicAuth(
                username=self._config.get('API', 'User'),
                password=self._config.get('API', 'Password')
            )
        )

    def extract_timetables(self, api_load, limit=2):
        timetables_list = []
        tree = etree.fromstring(api_load.text.encode('utf-8'))

        for train in tree.xpath('/passages/train')[:limit]:
            formatted_timetables = self.timetable_formatter(
                miss=train.find('miss').text,
                date=train.find('date').text
            )
            timetables_list.append(formatted_timetables)
        timetables_list.reverse()

        return timetables_list

    def display_timetables(self, timetables):
        # with canvas(self._display_device) as draw:
        #     for msg in messages:
        #         text(draw, (0, 9), "World", fill="white", font=proportional(LCD_FONT))
        for timetable in timetables:
            print(timetable)

    def manage_refresh_time(self):
        time.sleep(self._refresh_time)

    def increase_refresh_time(self):
        if self._refresh_time < self._max_refresh_time:
            self._refresh_time += self._step_refresh_time

    def timetable_formatter(self, miss, date):
        date_train = datetime.strptime(date, self._api_date_format)
        diff = date_train - datetime.now()
        date = timedelta_formatter(diff)

        return ("{miss}: {date}".format(miss=miss, date=date))


if __name__ == "__main__":
    try:
        bootstrap()
    except KeyboardInterrupt:
        pass
