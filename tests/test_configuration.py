import os

import pytest

from transilienwatcher.configuration import ConfigLoader
from transilienwatcher.exceptions import ConfigError


def test_rerwatcher_load_config_success(mocker):
    mocker.patch.dict(os.environ, {'TRANSILIEN__URL': 'http://test.url'})

    config = ConfigLoader.load()

    assert config['transilien']['url'] == 'http://test.url'
    assert config['display']['type'] == 'console'


def test_rerwatcher_load_config_fails():
    with pytest.raises(ConfigError):
        ConfigLoader.load('no-config.yml')
