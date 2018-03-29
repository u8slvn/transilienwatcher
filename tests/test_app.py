#!/usr/bin/env python3
# coding: utf-8

from datetime import timedelta
from unittest.mock import patch, Mock, MagicMock

import pytest
from freezegun import freeze_time

from rerwatcher import app


@patch('rerwatcher.app.RawConfigParser')
def test_load_config_return_data(rawconfigparser_mock):
    # GIVEN
    config_mock = MagicMock()
    config_mock.configure_mock(name='FOO-CONFIG')
    rawconfigparser_mock.return_value = config_mock

    # WHEN
    config = app.load_config()

    # THEN
    assert config.name == 'FOO-CONFIG'


@patch('rerwatcher.app.RerWatcher')
@patch('rerwatcher.app.matrix_device_builder')
@patch('rerwatcher.app.TransilienApiDriver')
@patch('rerwatcher.app.load_config')
def test_bootstrap_should_create_an_app(load_config_mock,
                                        api_driver_mock,
                                        device_builder_mock,
                                        app_mock):
    # GIVEN
    load_config_mock.return_value = 'FOO-CONFIG'
    api_driver_mock.return_value = 'FOO-API-DRIVER'
    device_builder_mock.return_value = 'FOO-DEVICE-BUILDER'

    # WHEN
    app.bootstrap()

    # THEN
    app_mock.assert_called_with(config='FOO-CONFIG',
                                api_driver='FOO-API-DRIVER',
                                display_device='FOO-DEVICE-BUILDER')


class TestRerWatcher:
    def setup(self):
        self.app = app.RerWatcher(
            config=Mock(), api_driver=Mock(), display_device=Mock()
        )

    @patch('rerwatcher.app.requests.get')
    def test_fetch_api_should_return_data(self, requests_mock):
        # GIVEN
        requests_mock.return_value = 'FOO-DATA'

        # WHEN
        data = self.app._fetch_api()

        # THEN
        assert data == 'FOO-DATA'

    @patch('rerwatcher.app.time.sleep')
    def test_manage_refresh_time_should_call_sleep(self, time_mock):
        # GIVEN
        self.app._refresh_time = 10

        # WHEN
        self.app._manage_refresh_time()

        # THEN
        time_mock.assert_called_with(10)

    @pytest.mark.parametrize('times,expected', [
        (1, 20),
        (2, 30),
        (3, 30),
    ])
    def test_increase_refresh_time(self, times, expected):
        # GIVEN
        self.app._refresh_time = 10
        self.app._refresh_time_max = 30
        self.app._refresh_time_step = 10

        # WHEN
        for _ in range(times):
            self.app._increase_refresh_time()

        # THEN
        assert self.app._refresh_time is expected


class TestTransilienApiDriver:
    def setup(self):
        self.api_driver = app.TransilienApiDriver(Mock())
        self.api_driver._date_format = '%d/%m/%Y %H:%M'
        self.api_driver._encoding = 'utf-8'

    @pytest.mark.parametrize("given,expected", [
        (timedelta(seconds=40), '1min',),
        (timedelta(seconds=120), '2min',),
        (timedelta(seconds=7400), '2h',),
    ])
    def test_timedelta_formatter(self, given, expected):
        assert self.api_driver._timedelta_formatter(given) == expected

    @freeze_time("27-10-2018 13:30")
    def test_convert_date_to_time(self):
        # GIVEN
        api_driver = self.api_driver
        api_driver._timedelta_formatter = Mock(return_value='2min')
        date_str = '27/10/2018 13:32'

        # WHEN
        time = api_driver._convert_date_to_time(date_str=date_str)

        # THEN
        assert time == '2min'
        api_driver._timedelta_formatter.assert_called_once_with(
            timedelta(seconds=120))

    @patch('rerwatcher.app.TimeTable')
    @patch('rerwatcher.app.etree')
    def test_extract_timetables_should_return_two_elements(
            self,
            etree_mock,
            timetable_mock
    ):
        # GIVEN
        api_driver = self.api_driver
        api_driver._convert_date_to_time = Mock()
        tree_mock = Mock()
        tree_mock.xpath.return_value = [Mock(), Mock()]
        etree_mock.fromstring.return_value = tree_mock
        timetable_mock.side_effect = ['FOO', 'BAR']

        # WHEN
        result_list = api_driver.get_timetables(Mock())

        # THEN
        assert result_list == ['FOO', 'BAR']
        assert len(api_driver._convert_date_to_time.call_args_list) is 2


class TestTimeTable:
    def test_display(self):
        # GIVEN
        timetable = app.TimeTable('FOO', 'BAR')

        # WHEN
        message = timetable.display()

        # THEN
        assert message == 'FOO: BAR'
