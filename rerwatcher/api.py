from string import Template

import requests
from loguru import logger
from requests import RequestException, ReadTimeout
from requests.auth import HTTPBasicAuth


class TransilienApi:
    def __init__(self, config):
        url_template = Template(config['api']['url'])
        self._url = url_template.substitute(
            departure_station=config['api']['departure_station'],
            arrival_station=config['api']['arrival_station']
        )
        self._auth = HTTPBasicAuth(
            username=config['api']['user'],
            password=config['api']['password']
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
