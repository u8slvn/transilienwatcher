#!/usr/bin/env python3
# coding: utf-8

from datetime import datetime

from lxml import etree
import requests
from requests.auth import HTTPBasicAuth


class TransilienApi:
    def __init__(self, config):
        self._url = config.get('api', 'url')
        self._auth = HTTPBasicAuth(
            username=config.get('api', 'user'),
            password=config.get('api', 'password')
        )
        self._date_format = config.get('api', 'date_format')
        self._encoding = config.get('api', 'encoding')

    def fetch_data(self):
        response = requests.get(url=self._url, auth=self._auth)
        timetables = self._get_timetables(response)

        return timetables

    def _get_timetables(self, response, limit=2):
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
