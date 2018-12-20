#!/usr/bin/env python3
# coding: utf-8
""" RERWatcher Api

This module provides simple tools to manage the transilien api and
format every response data fetched from it.

"""

from datetime import datetime

import requests
from lxml import etree
from requests.auth import HTTPBasicAuth


def calculate_time_delta_with_now(date, date_format):
    """Calculate the time delta between now and a given date

    Args:
        date (str): the date to calculate with now.
        date_format (str): the format to cast the date.

    Returns:
        timedelta (timedelta): the result of the dates.

    """
    date = datetime.strptime(date, date_format)
    timedelta = date - datetime.now()

    return timedelta


def format_timedelta(timedelta):
    """Format timedelta for human readability

    Args:
        timedelta (timedelta): the timedelta to format.

    Returns:
        time (str): timedelta formated to string.

    """
    hours = timedelta.seconds // 3600
    minutes = (timedelta.seconds // 60) % 60
    if minutes < 1:
        minutes = 1

    time = "{}min".format(minutes)
    if hours > 1:
        time = "{}h".format(hours)

    return time


class TransilienApi:
    """Translien api

    This class allows to manage the transilien api by requesting and
    formatting its data.

    Args:
        config (dict): the config must contain an 'api' key containing
            all the mandatory data: 'url', 'departure_station',
            'arrival_sation', 'user', 'password', 'date_format',
            'encoding'.

    Attributes:
        _url (str): https://api.transilien.com/gare/{departure_station}/depart/{arrival_station}
        _auth (HTTPBasicAuth): the basic authentication built with the
            user and password config params.
        _date_format (str): '%d/%m/%Y %H:%M'
        _encoding (str): 'utf-8'

    """

    def __init__(self, config):
        self._url = config['api']['url'].format(
            departure_station=config['api']['departure_station'],
            arrival_station=config['api']['arrival_station']
        )
        self._auth = HTTPBasicAuth(
            username=config['api']['user'],
            password=config['api']['password']
        )
        self._date_format = config['api']['date_format']
        self._encoding = config['api']['encoding']

    def fetch_data(self):
        """Fetch api data

        Fetch data from the api and extract and format them to Timetable.

        Returns:
            timetables (list<TimeTable>): the next departure timetable.
        """
        response = requests.get(url=self._url, auth=self._auth)
        timetables = self._get_timetables(response)

        return timetables

    def _get_timetables(self, response, limit=2):
        """Parse response and extract the two next timetables."""
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
    """Timetable

    Encapsulate timetable information.

    Attributes:
        miss (str): the train code.
        time: the departure time.

    """

    def __init__(self, miss, time):
        self.miss = miss
        self.time = time

    def text(self):
        """Return the timetable to nice format."""
        return ("{miss}: {time}".format(miss=self.miss, time=self.time))
