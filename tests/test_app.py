#!/usr/bin/env python3
# coding: utf-8

import os
from unittest.mock import patch, Mock

import pytest
from rerwatcher import app


def test_load_config_return_data_with_environment_value():
    # WHEN
    with patch.dict(os.environ, {'API_URL': 'http://test.url'}):
        config = app.load_config()

    # THEN
    assert config['api']['url'] == 'http://test.url'
    assert config['device']['type'] == 'console'


@patch('rerwatcher.app.RerWatcher')
@patch('rerwatcher.app.DisplayDeviceFactory')
@patch('rerwatcher.app.load_config')
def test_bootstrap_should_create_an_app(load_config_mock,
                                        display_device_factory_mock,
                                        app_mock):
    # GIVEN
    load_config_mock.return_value = 'FOO-CONFIG'
    display_device_factory_mock.build.return_value = 'FOO-DEVICE-BUILDER'

    # WHEN
    app.build_rer_watcher()

    # THEN
    app_mock.assert_called_with(config='FOO-CONFIG',
                                display='FOO-DEVICE-BUILDER')


class TestRerWatcher:
    def setup(self):
        self.app = app.RerWatcher(
            config=Mock(), display=Mock()
        )

    @patch('rerwatcher.api.requests')
    def test_fetch_api_should_return_data(self, requests):
        # GIVEN
        self.app._api._get_timetables = Mock()
        self.app._api._get_timetables.return_value = 'FOO-DATA'

        # WHEN
        data = self.app._api.fetch_data()

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
