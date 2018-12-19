#!/usr/bin/env python3
# coding: utf-8

from datetime import datetime

import requests
from lxml import etree
from requests.auth import HTTPBasicAuth


def calculate_time_delta_with_now(date, date_format):
    date = datetime.strptime(date, date_format)
    timedelta = date - datetime.now()

    return timedelta


def format_timedelta(timedelta):
    hours = timedelta.seconds // 3600
    minutes = (timedelta.seconds // 60) % 60
    if minutes < 1:
        minutes = 1

    time_str = "{}min".format(minutes)
    if hours > 1:
        time_str = "{}h".format(hours)

    return time_str


class TransilienApi:
    def __init__(self, config):
        self._url = config['api']['url']
        self._auth = HTTPBasicAuth(
            username=config['api']['user'],
            password=config['api']['password']
        )
        self._date_format = config['api']['date_format']
        self._encoding = config['api']['encoding']

    def fetch_data(self):
        response = requests.get(url=self._url, auth=self._auth)
        timetables = self._get_timetables(response)

        return timetables

    def _get_timetables(self, response, limit=2):
        response_body = response.text.encode(self._encoding)

        tree = etree.fromstring(response_body)
        trains = tree.xpath('/passages/train')

        timetables = list()

        for train in trains[:limit]:
            miss = train.find('miss').text
            date = train.find('date').text

            timedelta = calculate_time_delta_with_now(
                date=date,
                date_format=self._date_format
            )
            time = format_timedelta(timedelta=timedelta)

            timetable = TimeTable(miss=miss, time=time)

            timetables.append(timetable)

        return timetables


class TimeTable:
    def __init__(self, miss, time):
        self.miss = miss
        self.time = time

    def text(self):
        return ("{miss}: {time}".format(miss=self.miss, time=self.time))
