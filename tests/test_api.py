from string import Template

from freezegun import freeze_time
from requests.auth import HTTPBasicAuth

from rerwatcher.api import TransilienApi
from tests.conftest import CONFIG


def load_fixture(fake_config):
    with open('tests/fixture.xml') as file:
        data = file.read()

    return data.encode(fake_config['api']['encoding'])


class TestTransilienApiDriver:
    def test_init(self):
        api_config = CONFIG['api']
        api = TransilienApi(api_config)

        assert api._url == Template(api_config['url']).substitute(
            departure_station=api_config['departure_station'],
            arrival_station=api_config['arrival_station'],
        )
        assert isinstance(api._auth, HTTPBasicAuth)

    @freeze_time("27-10-2018 13:30")
    def test_fetch_data_return_two_timetables(self, mocker):
        requests = mocker.patch('rerwatcher.api.requests')
        api = TransilienApi(CONFIG['api'])

        api.fetch_data()

        requests.get.assert_called_once_with(
            url=api._url,
            auth=api._auth
        )
