import os

import yaml
from cerberus import Validator

from transilienwatcher.exceptions import (
    ConfigError,
    InvalidConfigError,
    ConfigNotFoundError,
)

DEFAULT_CONFIG = {
    "transilien": {
        "stations": {
            "departure": None,
            "arrival": None,
        },
        "credentials": {
            "username": None,
            "password": None,
        },
    },
    "refresh_time": 30,
    "display": {
        "type": None,
        "lcd": {
            "columns": 16,
            "rows": 2,
        },
    },
}

departure_schema = {
    "required": True,
    "nullable": False,
    "type": "string",
    "regex": "\\d{8}",
}
arrival_schema = {
    "required": False,
    "nullable": True,
    "type": "string",
    "regex": "\\d{8}",
}
credential_schema = {
    "required": True,
    "nullable": False,
    "type": "string",
}
lcd_size_schema = {
    "required": True,
    "nullable": False,
    "type": "integer",
}
display_schema = {
    "type": "dict",
    "schema": {
        "type": {
            "required": True,
            "type": "string",
            "oneof": [
                {"dependencies": "lcd", "allowed": ["lcd"]},
                {"allowed": ["console"]},
            ],
        },
        "lcd": {
            "required": False,
            "schema": {
                "columns": lcd_size_schema,
                "rows": lcd_size_schema,
            },
        },
    },
}
config_schema = {
    "transilien": {
        "type": "dict",
        "schema": {
            "stations": {
                "type": "dict",
                "schema": {
                    "departure": departure_schema,
                    "arrival": arrival_schema,
                },
            },
            "credentials": {
                "type": "dict",
                "schema": {
                    "username": credential_schema,
                    "password": credential_schema,
                },
            },
        },
    },
    "refresh_time": {"type": "integer"},
    "display": display_schema,
}
config_validator = Validator(config_schema)


class ConfigManager:
    @classmethod
    def load(cls, file: str) -> dict:
        config = dict(DEFAULT_CONFIG)
        cls.update_config(config, cls._load_file(file=file))
        config.update(cls.overwrite_config_with_env(config=config))
        if not config_validator.validate(config):
            raise InvalidConfigError(
                f"Invalid configuration provided.\n {config_validator.errors}"
            )
        return config

    @staticmethod
    def _load_file(file: str) -> dict:
        try:
            with open(file, "r") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError as error:
            raise ConfigNotFoundError(
                f"Configuration file {file} not found."
            ) from error
        return config

    @classmethod
    def create(cls, file: str):
        try:
            with open(file, "x") as f:
                f.write(yaml.dump(DEFAULT_CONFIG))
        except FileExistsError as error:
            raise ConfigError(f"Configuration file {file} already exists.") from error

    @classmethod
    def overwrite_config_with_env(cls, config: dict, _path=None):
        """Iterate over config dict and upload value with env vars."""
        path = _path or []
        env_key = "__".join(path).upper()

        if isinstance(config, dict):
            for index, value in config.items():
                path.append(index)
                config[index] = cls.overwrite_config_with_env(value, path)
                del path[-1]
        elif os.environ.get(env_key):
            return os.environ.get(env_key)

        return config

    @classmethod
    def update_config(cls, source: dict, update: dict):
        """Update dict config without modifying its structure."""
        for key, value in update.items():
            if isinstance(value, dict) and key in source:
                cls.update_config(source[key], update[key])
            else:
                source[key] = update[key]
