from string import Template

from freezegun import freeze_time
from requests.auth import HTTPBasicAuth

from rerwatcher.api import TransilienApi
from tests.conftest import FAKE_CONFIG


def load_fixture(fake_config):
    with open('tests/fixture.xml') as file:
        data = file.read()

    return data.encode(fake_config['api']['encoding'])


class TestTransilienApiDriver:
    def test_init(self):
        api = TransilienApi(FAKE_CONFIG)

        assert api._url == Template(FAKE_CONFIG['api']['url']).substitute(
            departure_station=FAKE_CONFIG['api']['departure_station'],
            arrival_station=FAKE_CONFIG['api']['arrival_station'],
        )
        assert isinstance(api._auth, HTTPBasicAuth)

    @freeze_time("27-10-2018 13:30")
    def test_fetch_data_return_two_timetables(self, mocker):
        requests = mocker.patch('rerwatcher.api.requests')
        api = TransilienApi(FAKE_CONFIG)

        api.fetch_data()

        requests.get.assert_called_once_with(
            url=api._url,
            auth=api._auth
        )
