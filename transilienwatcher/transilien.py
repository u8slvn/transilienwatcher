from datetime import datetime, timedelta

import requests
from loguru import logger
from lxml import etree
from requests.auth import HTTPBasicAuth

from transilienwatcher import error_handlers
from transilienwatcher.exceptions import RequestError


class Requester:
    def __init__(self, url: str, username: str, password: str):
        self._url = url
        self._auth = HTTPBasicAuth(
            username=username,
            password=password
        )

    @error_handlers.request_data
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

    @error_handlers.format_data
    def format(self, data: str, limit: int = 2):
        data = data.encode(self.encoding)
        logger.info(f"Formatting data {data or 'None'}.")

        tree = etree.fromstring(data)
        trains = tree.xpath('/passages/train')

        timetables = [self._format_train(train) for train in trains[:limit]]
        return timetables

    def _format_train(self, train):
        miss = train.find('miss').text  # Mission code of the train.
        date = train.find('date').text
        status = train.find('etat')

        status = status if status is None else status.text

        date = datetime.strptime(date, self.date_format)
        time_delta = date - datetime.now()

        time = self._format_timedelta(time_delta=time_delta)
        timetable = f'{miss}: {status or time}'
        return timetable

    @staticmethod
    def _format_timedelta(time_delta: timedelta):
        hours = time_delta.seconds // 3600
        minutes = (time_delta.seconds // 60) % 60
        time = f"{hours}h{minutes:02d}" if hours > 1 else f"{minutes}min"
        return time


class Transilien:
    def __init__(self, config: dict):
        self.requester = Requester(**config)
        self.formatter = Formatter()

    @error_handlers.fetch_data
    def fetch_data(self):
        data = self.requester.request()
        data = self.formatter.format(data=data)
        return data
