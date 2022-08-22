import os
from pathlib import Path

import pytest

from transilienwatcher.configuration import ConfigManager
from transilienwatcher.exceptions import (
    ConfigError,
    ConfigNotFoundError,
    InvalidConfigError,
)

HERE = Path(__file__).parent.absolute()


def test_load_config_success():
    config = ConfigManager.load(file=f"{HERE}/configs/config.yml")

    assert "transilien" in config
    assert "refresh_time" in config
    assert "display" in config


def test_load_no_config_fails():
    with pytest.raises(ConfigNotFoundError):
        ConfigManager.load(file="no-config.yml")


def test_load_invalid_config_fails():
    with pytest.raises(InvalidConfigError):
        ConfigManager.load(file=f"{HERE}/configs/invalid.yml")


def test_create_config(cleanup_files):
    config = f"{HERE}/test_config.yml"
    ConfigManager.create(file=config)

    assert Path(config).is_file()


def test_create_config_fails_if_already_exists(cleanup_files):
    config = f"{HERE}/test_config.yml"
    ConfigManager.create(file=config)

    with pytest.raises(ConfigError):
        ConfigManager.create(file=config)


def test_overwrite_config_with_env(mocker):
    mocker.patch.dict(
        os.environ,
        {
            "FOO__BAR": "foobar",
        },
    )
    config = {"foo": {"bar": None}}

    result = ConfigManager.overwrite_config_with_env(config)

    assert result["foo"]["bar"] == "foobar"


def test_update_config():
    source_config = {"foo": {"bar": "barfoo", "test": True}}
    update_config = {"foo": {"bar": "foobar"}}

    ConfigManager.update_config(source=source_config, update=update_config)

    assert source_config == {"foo": {"bar": "foobar", "test": True}}
