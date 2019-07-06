#!/usr/bin/env python3
# coding: utf-8

from datetime import timedelta
from string import Template
from unittest.mock import patch, Mock

import pytest
from freezegun import freeze_time
from requests.auth import HTTPBasicAuth

from rerwatcher.api import TransilienApi, TimeTable, format_timedelta, \
    calculate_time_delta_with_now
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
    @patch('rerwatcher.api.requests')
    def test_fetch_data_return_two_timetables(self, requests):
        response = Mock()
        response.text.encode.return_value = load_fixture(FAKE_CONFIG)
        requests.get = Mock()
        requests.get.return_value = response

        api = TransilienApi(FAKE_CONFIG)
        data = api.fetch_data()

        assert 2 == len(data)
        assert isinstance(data[0], TimeTable)
        assert data[0].text() == 'DACA: 8h'
        assert isinstance(data[1], TimeTable)
        assert data[1].text() == 'FACA: 9h'


class TestTimeTable:
    def test_text(self):
        timetable = TimeTable('FOO', 'BAR')

        message = timetable.text()

        assert message == 'FOO: BAR'


@pytest.mark.parametrize("given,expected", [
    (timedelta(seconds=40), '1min',),
    (timedelta(seconds=120), '2min',),
    (timedelta(seconds=7400), '2h',),
])
def test_format_timedelta(given, expected):
    assert format_timedelta(given) == expected


@freeze_time("27-10-2018 13:30")
def test_calculate_time_delta_with_now():
    date_str = '27/10/2018 13:32'

    time_delta = calculate_time_delta_with_now(
        date=date_str,
        date_format=FAKE_CONFIG['api']['date_format']
    )

    assert time_delta == timedelta(seconds=120)
