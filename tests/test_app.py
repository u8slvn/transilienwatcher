#!/usr/bin/env python3
# coding: utf-8

from configparser import RawConfigParser
from datetime import timedelta
from unittest.mock import patch, Mock

import pytest
from freezegun import freeze_time

from rerwatcher import app


@pytest.mark.parametrize("given,expected", [
    (timedelta(seconds=40), '1min',),
    (timedelta(seconds=120), '2min',),
    (timedelta(seconds=7400), '2h',),
])
def test_timedelta_formatter(given, expected):
    assert app.timedelta_formatter(given) == expected


@patch('rerwatcher.app.RERWatcher')
@patch('rerwatcher.app.matrix_device_builder')
@patch('rerwatcher.app.RawConfigParser.read')
def test_bootstrap_should_create_an_app(rawconfigparser_mock,
                                        device_builder_mock,
                                        app_mock):
    # GIVEN
    device_builder_mock.return_value = 'FOO-DEVICE-BUILDER'

    # WHEN
    app.bootstrap()

    # THENself.app
    expected_config = RawConfigParser()
    app_mock.assert_called_with(config=expected_config,
                                display_device='FOO-DEVICE-BUILDER')


@freeze_time("27-10-2018 13:30")
class TestRERWatcher:
    def setup(self):
        mock = Mock()
        self.app = app.RERWatcher(mock, mock)
        self.app._api_date_format = '%d/%m/%Y %H:%M'

    @patch('rerwatcher.app.timedelta_formatter')
    def test_timetable_formatter_should_return_str(self,
                                                   timedelta_formatter_mock):
        # GIVEN
        miss = 'FOO'
        date = '27/10/2018 13:39'
        timedelta_formatter_mock.return_value = '9min'

        # WHEN
        result_timetale = self.app.timetable_formatter(miss=miss, date=date)

        # THEN
        expected_timetable = 'FOO: 9min'
        assert result_timetale == expected_timetable

    @patch('rerwatcher.app.timedelta_formatter')
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

    @patch('rerwatcher.app.requests.get')
    def test_fetch_api_sould_return_data(self, requests_mock):
        # GIVEN
        requests_mock.return_value = 'FOO-DATA'

        # WHEN
        result_data = self.app.fetch_api()

        # THEN
        expected_data = 'FOO-DATA'
        assert result_data == expected_data

    @patch('rerwatcher.app.time.sleep')
    def test_manage_refresh_time_should_call_sleep(self, time_mock):
        # GIVEN
        self.app._refresh_time = 10

        # WHEN
        self.app.manage_refresh_time()

        # THEN
        time_mock.assert_called_with(10)

    def test_get_response_text_encoded_should_return_data(self):
        # GIVEN
        data_mock = Mock()
        data_mock.text.encode.return_value = 'FOO-DATA'

        # WHEN
        result_data = app.get_text_response_encoded(data_mock)

        # THEN
        expected_data = 'FOO-DATA'
        assert result_data == expected_data

    @patch('rerwatcher.app.RERWatcher.timetable_formatter')
    @patch('rerwatcher.app.etree')
    def test_extract_timetables_should_return_two_elements(
            self,
            etree_mock,
            timetable_formatter_mock
    ):
        # GIVEN
        tree_mock = Mock()
        tree_mock.xpath.return_value = [Mock(name=1), Mock(name=2)]
        etree_mock.fromstring.return_value = tree_mock
        timetable_formatter_mock.side_effect = ['FOO-ONE', 'FOO-TWO']

        # WHEN
        result_list = self.app.extract_timetables(None)

        # THEN
        expected_list = ['FOO-TWO', 'FOO-ONE']
        assert result_list == expected_list
        assert len(timetable_formatter_mock.call_args_list) is 2
