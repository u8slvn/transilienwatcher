import os

import pytest

from transilienwatcher.configuration import ConfigLoader
from transilienwatcher.exceptions import ConfigError


def test_rerwatcher_load_config_success(mocker):
    mocker.patch.dict(os.environ, {
        'TRANSILIEN__STATIONS__DEPARTURE': '45609890',
    })

    config = ConfigLoader.load()

    assert config['transilien']['stations']['departure'] == '45609890'
    assert config['display']['type'] == 'lcd'


def test_rerwatcher_load_config_fails():
    with pytest.raises(ConfigError):
        ConfigLoader.load('no-config.yml')
