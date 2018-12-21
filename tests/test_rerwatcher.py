#!/usr/bin/env python3
# coding: utf-8

import os
from string import Template
from unittest.mock import patch

from requests.auth import HTTPBasicAuth

import rerwatcher
from rerwatcher.api import TransilienApi
from rerwatcher.app import RerWatcher
from rerwatcher.display import DisplayDevice


def test_load_config_return_data_with_environment_value():
    with patch.dict(os.environ, {'API_URL': 'http://test.url'}):
        config = rerwatcher.load_config()

    assert config['api']['url'] == 'http://test.url'
    assert config['device']['type'] == 'console'


@patch('rerwatcher.load_config')
def test_build_rer_watcher_return_app(load_config, fake_config):
    load_config.return_value = fake_config

    app = rerwatcher.build_rer_watcher()

    assert isinstance(app, RerWatcher)
    assert app._refresh_time == fake_config['refresh_time']['default']
    assert isinstance(app._api, TransilienApi)
    assert app._api._url == Template(fake_config['api']['url']).substitute(
        departure_station=fake_config['api']['departure_station'],
        arrival_station=fake_config['api']['arrival_station'],
    )
    assert isinstance(app._api._auth, HTTPBasicAuth)
    assert isinstance(app._display, DisplayDevice)
