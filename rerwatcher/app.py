#!/usr/bin/env python3
# coding: utf-8

import time
from abc import abstractmethod, ABCMeta
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


def load_config():
    config = RawConfigParser()
    config.read('settings.ini')

    return config


def bootstrap():
    config = load_config()

    api_driver = TransilienApiDriver(config)

    matrix_device = DisplayDeviceFactory.build(config)

    app = RerWatcher(
        config=config,
        api_driver=api_driver,
        display_device=matrix_device
    )
    app.start()


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


class TransilienApiDriver:
    def __init__(self, config):
        self._date_format = config.get('api', 'date_format')
        self._encoding = config.get('api', 'encoding')

    def get_timetables(self, response, limit=2):
        response_body = response.text.encode(self._encoding)

        tree = etree.fromstring(response_body)
        trains = tree.xpath('/passages/train')

        timetables_list = list()

        for train in trains[:limit]:
            miss = train.find('miss').text
            date = train.find('date').text

            date = self._convert_date_to_time(date)

            timetable = TimeTable(miss=miss, date=date)

            timetables_list.append(timetable)

        return timetables_list

    def _convert_date_to_time(self, date_str):
        date = datetime.strptime(date_str, self._date_format)
        diff = date - datetime.now()
        time = self._timedelta_formatter(diff)

        return time

    def _timedelta_formatter(self, time_value):
        hours = time_value.seconds // 3600
        minutes = (time_value.seconds // 60) % 60
        if minutes < 1:
            minutes = 1

        time_str = "{}min".format(minutes)
        if hours > 1:
            time_str = "{}h".format(hours)

        return time_str


class TimeTable:
    def __init__(self, miss, date):
        self.miss = miss
        self.date = date

    def text(self):
        return ("{miss}: {date}".format(miss=self.miss, date=self.date))


class DisplayDevice(metaclass=ABCMeta):
    @abstractmethod
    def print(self, messages):
        raise NotImplementedError


class ConsoleDisplay(DisplayDevice):
    def print(self, messages):
        for message in messages:
            print(message.text())


class MatrixDisplay(DisplayDevice):
#     def __init__(self):
#         serial = spi(port=0, device=0, gpio=noop())
#         self._device = max7219(
#             serial, width=64, height=16, block_orientation=-90, rotate=0
#         )
#         self._device.contrast(32)
#
    def display(self, messages):
        pass
#         with canvas(self._device) as draw:
#             for message in messages:
#                 text(draw, (0, 9), message.text(),
#                      fill="white", font=proportional(LCD_FONT)
#                 )


class DisplayDeviceFactory:
    @staticmethod
    def build(config):
        type = config.get('device', 'type')
        if type == 'matrix':
            return MatrixDisplay()
        if type == 'console':
            return ConsoleDisplay()

        raise NotImplementedError


if __name__ == "__main__":
    try:
        bootstrap()
    except KeyboardInterrupt:
        pass
