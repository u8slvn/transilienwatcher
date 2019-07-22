from datetime import datetime, timedelta

import requests
from loguru import logger
from lxml import etree
from requests.auth import HTTPBasicAuth

from rerwatcher.exceptions import (request_error_handler, format_error_handler,
                                   RequestError, fetch_data_error_handler)


class Requester:
    def __init__(self, config: dict):
        self._url = config['url']
        self._auth = HTTPBasicAuth(
            username=config['user'],
            password=config['password']
        )

    @request_error_handler
    def request(self):
        logger.info(f"Fetching data from {self._url}.")
        response = requests.get(url=self._url, auth=self._auth)

        if response.status_code != 200:
            logger.error("Request failed.")
            raise RequestError(f"HTTP: {response.status_code} error")

        return response.text


class Formatter:
    encoding = 'utf-8'
    date_format = '%d/%m/%Y %H:%M'

    @format_error_handler
    def format(self, data: str, limit: int = 2):
        data = data.encode(self.encoding)
        logger.info(f"Formatting data {data or 'None'}.")

        tree = etree.fromstring(data)
        trains = tree.xpath('/passages/train')

        timetables = [self._format_train(train) for train in trains[:limit]]
        return timetables

    def _format_train(self, train):
        miss = train.find('miss').text
        date = train.find('date').text

        date = datetime.strptime(date, self.date_format)
        time_delta = date - datetime.now()

        time = self._format_timedelta(time_delta=time_delta)
        timetable = f'{miss}: {time}'
        return timetable

    @staticmethod
    def _format_timedelta(time_delta: timedelta):
        hours = time_delta.seconds // 3600
        minutes = (time_delta.seconds // 60) % 60
        time = f"{hours}h{minutes:02d}" if hours > 1 else f"{minutes}min"
        return time


class Transilien:
    def __init__(self, config):
        self.requester = Requester(config)
        self.formatter = Formatter()

    @fetch_data_error_handler
    def fetch_data(self):
        data = self.requester.request()
        data = self.formatter.format(data=data)
        return data
