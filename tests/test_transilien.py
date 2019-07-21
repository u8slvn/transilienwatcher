from unittest.mock import sentinel

import pytest
from freezegun import freeze_time
from requests import HTTPError, RequestException
from requests.auth import HTTPBasicAuth

from rerwatcher.exceptions import RequestError, FormatError
from rerwatcher.transilien import Requester, Formatter, Transilien


class TestRequester:
    def test_request(self, mocker, config):
        requests = mocker.patch('rerwatcher.transilien.requests.get')
        requester = Requester(config['api'])

        requester.request()

        url = config['api']['url']
        auth = HTTPBasicAuth(
            username=config['api']['user'],
            password=config['api']['password']
        )
        requests.assert_called_once_with(url=url, auth=auth)

    @pytest.mark.parametrize('exception', [HTTPError, RequestException])
    def test_request_fails(self, mocker, config, exception):
        mocker.patch(
            'rerwatcher.transilien.requests.get',
            side_effect=exception
        )
        requester = Requester(config['api'])

        with pytest.raises(RequestError):
            requester.request()


class TestFormatter:
    @freeze_time("27-10-2018 20:10")
    def test_format(self, requests_fixture):
        formatter = Formatter()

        result = formatter.format(requests_fixture)

        assert ['DACA: 6min', 'FACA: 3h'] == result

    def test_format_fails(self, mocker):
        mocker.patch(
            'rerwatcher.transilien.etree.fromstring',
            side_effect=Exception
        )
        formatter = Formatter()

        with pytest.raises(FormatError):
            formatter.format()


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
