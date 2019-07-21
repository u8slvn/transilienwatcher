from unittest.mock import sentinel

from freezegun import freeze_time
from requests.auth import HTTPBasicAuth

from rerwatcher.transilien import Requester, Formatter, Transilien


class TestRequester:
    def test_request(self, mocker, config):
        requests = mocker.patch('rerwatcher.transilien.requests.get')
        rrequester = Requester(config['api'])

        rrequester.request()

        url = config['api']['url']
        auth = HTTPBasicAuth(
            username=config['api']['user'],
            password=config['api']['password']
        )
        requests.assert_called_once_with(url=url, auth=auth)


class TestFormatter:
    @freeze_time("27-10-2018 20:10")
    def test_format(self, requests_fixture):
        formatter = Formatter()

        result = formatter.format(requests_fixture)

        assert ['DACA: 6min', 'FACA: 3h'] == result


class TestTransilien:
    def test_fetch_data(self, mocker, config):
        mocker.patch(
            'rerwatcher.transilien.Requester.request',
            return_value=sentinel.raw_data
        )
        formatter = mocker.patch(
            'rerwatcher.transilien.Formatter.format',
            return_value=sentinel.data
        )
        transilien = Transilien(config['api'])

        result = transilien.fetch_data()

        assert result == sentinel.data
        formatter.assert_called_once_with(data=sentinel.raw_data)
