#!/usr/bin/env python3
# coding: utf-8

from unittest.mock import patch, Mock, MagicMock

import pytest
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
@patch('rerwatcher.app.DisplayDeviceFactory')
@patch('rerwatcher.app.TransilienApiDriver')
@patch('rerwatcher.app.load_config')
def test_bootstrap_should_create_an_app(load_config_mock,
                                        api_driver_mock,
                                        display_device_factory_mock,
                                        app_mock):
    # GIVEN
    load_config_mock.return_value = 'FOO-CONFIG'
    api_driver_mock.return_value = 'FOO-API-DRIVER'
    display_device_factory_mock.build.return_value = 'FOO-DEVICE-BUILDER'

    # WHEN
    app.build_rer_watcher()

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
