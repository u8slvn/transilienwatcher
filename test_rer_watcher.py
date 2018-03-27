#!/usr/bin/env python3
# coding: utf-8

from configparser import RawConfigParser
from datetime import timedelta
from unittest.mock import patch, Mock

import pytest
from freezegun import freeze_time

import rer_watcher


@pytest.mark.parametrize("given,expected", [
    (timedelta(seconds=40), '1min',),
    (timedelta(seconds=120), '2min',),
    (timedelta(seconds=120), '2min',),
])
def test_timedelta_formatter(given, expected):
    assert rer_watcher.timedelta_formatter(given) == expected


@patch('rer_watcher.RERWatcher')
@patch('rer_watcher.matrix_device_builder')
@patch('rer_watcher.RawConfigParser.read')
def test_bootstrap_should_create_an_app(rawconfigparser_mock,
                                        device_builder_mock,
                                        rer_watcher_mock):
    # GIVEN
    device_builder_mock.return_value = 'FOO-DEVICE-BUILDER'

    # WHEN
    rer_watcher.bootstrap()

    # THENself.app
    expected_config = RawConfigParser()
    rer_watcher_mock.assert_called_with(config=expected_config,
                                        display_device='FOO-DEVICE-BUILDER')


@freeze_time("27-10-2018 13:30")
class TestRERWatcher:
    def setup(self):
        mock = Mock()
        self.app = rer_watcher.RERWatcher(mock, mock)
        self.app._api_date_format = '%d/%m/%Y %H:%M'

    @patch('rer_watcher.timedelta_formatter')
    def test_timetable_formatter_should_return_str(self,
                                                   timedelta_formatter_mock):
        # GIVEN
        miss = 'FOO'
        date = '27/10/2018 13:39'
        timedelta_formatter_mock.return_value = '9min'

        # WHEN
        result = self.app.timetable_formatter(miss=miss, date=date)

        # THEN
        assert 'FOO: 9min' == result

    @patch('rer_watcher.timedelta_formatter')
    def test_timetable_formatter_should_call_timedelta_formatter(
            self,
            timedelta_formatter_mock
    ):
        # GIVEN
        miss = 'FOO'
        date = '27/10/2018 13:31'

        # WHEN
        self.app.timetable_formatter(miss=miss, date=date)

        # THEN
        expected_timedelta = timedelta(seconds=60)
        timedelta_formatter_mock.assert_called_with(expected_timedelta)
