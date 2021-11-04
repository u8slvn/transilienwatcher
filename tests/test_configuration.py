import os

import pytest

from transilienwatcher.configuration import ConfigLoader
from transilienwatcher.exceptions import ConfigError


def test_load_config_success():
    config = ConfigLoader.load(file="config.yml")

    assert 'transilien' in config
    assert 'refresh_time' in config
    assert 'display' in config


def test_load_config_fails():
    with pytest.raises(ConfigError):
        ConfigLoader.load(file='no-config.yml')


def test_overwrite_config_with_env(mocker):
    mocker.patch.dict(os.environ, {
        'FOO__BAR': 'foobar',
    })
    config = {
        'foo': {
            'bar': None
        }
    }

    result = ConfigLoader.overwrite_config_with_env(config)

    assert result['foo']['bar'] == 'foobar'


def test_update_config():
    source_config = {'foo': {'bar': 'barfoo', 'test': True}}
    update_config = {'foo': {'bar': 'foobar'}}

    ConfigLoader.update_config(source=source_config, update=update_config)

    assert source_config == {'foo': {'bar': 'foobar', 'test': True}}
