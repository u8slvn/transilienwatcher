from unittest.mock import sentinel

import pytest
from freezegun import freeze_time
from requests import HTTPError, RequestException
from requests.auth import HTTPBasicAuth

from transilienwatcher.exceptions import RequestError, FormatError
from transilienwatcher.transilien import Requester, Formatter, Transilien


class TestRequester:
    def test_request_success(self, mocker, config):
        config = config['transilien']['credentials']
        response = mocker.Mock()
        response.status_code = 200
        response.text = 'foo'
        requests = mocker.patch(
            'transilienwatcher.transilien.requests.get',
            return_value=response
        )
        requester = Requester(url='test.url', **config)

        result = requester.request()

        auth = HTTPBasicAuth(
            username=config['username'],
            password=config['password']
        )
        requests.assert_called_once_with(url='test.url', auth=auth)
        assert 'foo' == result

    def test_request_fails_if_response_is_not_200(self, mocker, config):
        config = config['transilien']['credentials']
        response = mocker.Mock()
        response.status_code = 403
        mocker.patch(
            'transilienwatcher.transilien.requests.get',
            return_value=response
        )
        requester = Requester(url='test.url', **config)

        with pytest.raises(RequestError):
            requester.request()

    @pytest.mark.parametrize('exception', [HTTPError, RequestException])
    def test_request_fails(self, mocker, config, exception):
        config = config['transilien']['credentials']
        mocker.patch(
            'transilienwatcher.transilien.requests.get',
            side_effect=exception
        )
        requester = Requester(url='test.url', **config)

        with pytest.raises(RequestError):
            requester.request()


class TestFormatter:
    @freeze_time("27-10-2018 20:10")
    def test_format_success(self, requests_fixture):
        formatter = Formatter()

        result = formatter.format(requests_fixture)

        assert ['DACA: 6min', 'FACA: 3h36'] == result

    @freeze_time("27-10-2018 20:10")
    def test_format_with_status(self, requests_fixture_status):
        formatter = Formatter()

        result = formatter.format(requests_fixture_status)

        assert ['DACA: Retardé', 'FACA: Supprimé'] == result

    def test_format_fails(self, mocker):
        mocker.patch(
            'transilienwatcher.transilien.etree.fromstring',
            side_effect=Exception
        )
        formatter = Formatter()

        with pytest.raises(FormatError):
            formatter.format()


class TestTransilien:
    @pytest.mark.parametrize('arrival, expected_url', [
        ('000001', 'https://api.transilien.com/gare/00000000/depart/000001'),
        (None, 'https://api.transilien.com/gare/00000000/depart/'),
    ])
    def test_init(self, mocker, config, arrival, expected_url):
        requester = mocker.patch('transilienwatcher.transilien.Requester')
        formatter = mocker.patch('transilienwatcher.transilien.Formatter')
        config['transilien']['stations']['arrival'] = arrival

        _ = Transilien(config['transilien'])

        requester.assert_called_once_with(
            url=expected_url,
            username='username',
            password='password'
        )
        formatter.assert_called_once()

    def test_fetch_data_success(self, mocker, config):
        mocker.patch(
            'transilienwatcher.transilien.Requester.request',
            return_value=sentinel.raw_data
        )
        formatter = mocker.patch(
            'transilienwatcher.transilien.Formatter.format',
            return_value=sentinel.data
        )
        transilien = Transilien(config['transilien'])

        result = transilien.fetch_data()

        assert result == sentinel.data
        formatter.assert_called_once_with(data=sentinel.raw_data)

    def test_fetch_data_fails_on_request(self, mocker, config):
        mocker.patch(
            'transilienwatcher.transilien.requests.get',
            side_effect=RequestException
        )
        formatter = mocker.patch(
            'transilienwatcher.transilien.Formatter.format'
        )
        transilien = Transilien(config['transilien'])

        result = transilien.fetch_data()

        assert ["HTTP: unknown error"] == result
        formatter.assert_not_called()

    def test_fetch_data_fails_on_format(self, mocker, config):
        mocker.patch(
            'transilienwatcher.transilien.Requester.request',
            return_value=sentinel.raw_data
        )
        mocker.patch(
            'transilienwatcher.transilien.etree.fromstring',
            side_effect=Exception
        )
        transilien = Transilien(config['transilien'])

        result = transilien.fetch_data()

        assert ["FORMAT: unknown error"] == result

    def test_fetch_data_fails(self, mocker, config):
        mocker.patch(
            'transilienwatcher.transilien.Requester.request',
            side_effect=Exception
        )
        transilien = Transilien(config['transilien'])

        with pytest.raises(Exception):
            transilien.fetch_data()
