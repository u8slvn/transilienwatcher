from string import Template

import requests
from loguru import logger
from requests import RequestException, ReadTimeout
from requests.auth import HTTPBasicAuth


class TransilienApi:
    def __init__(self, config):
        url_template = Template(config['url'])
        self._url = url_template.substitute(
            departure_station=config['departure_station'],
            arrival_station=config['arrival_station']
        )
        self._auth = HTTPBasicAuth(
            username=config['user'],
            password=config['password']
        )

    def fetch_data(self):
        data = None
        try:
            logger.info(f"Fetching data from {self._url}.")
            response = requests.get(url=self._url, auth=self._auth)
            data = response.text
        except (RequestException, ReadTimeout):
            logger.error(f"Fetching {self._url} failed.")

        return data
