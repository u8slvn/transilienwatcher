from datetime import datetime, timedelta

import requests
from loguru import logger
from lxml import etree
from requests import RequestException, ReadTimeout
from requests.auth import HTTPBasicAuth


class Requester:
    def __init__(self, config: dict):
        self._url = config['url']
        self._auth = HTTPBasicAuth(
            username=config['user'],
            password=config['password']
        )

    def request(self):
        try:
            logger.info(f"Fetching data from {self._url}.")
            response = requests.get(url=self._url, auth=self._auth)
        except (RequestException, ReadTimeout):
            logger.error(f"Fetching {self._url} failed.")
            raise

        return response.text


class Formatter:
    encoding = 'utf-8'
    date_format = '%d/%m/%Y %H:%M'

    def format(self, data: str, limit: int = 2):
        response_body = data.encode(self.encoding)
        tree = etree.fromstring(response_body)
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
        minutes = 1 if minutes < 1 else minutes

        time = f"{minutes}min"
        time = f"{hours}h" if hours > 1 else time
        return time


class Transilien:
    def __init__(self, config):
        self.requester = Requester(config)
        self.formatter = Formatter()

    def fetch_data(self):
        data = self.requester.request()
        data = self.formatter.format(data=data)
        return data
