import os

import yaml

from transilienwatcher.exceptions import ConfigError

default_config = {
    'transilien': {
        'url': None,
        'username': None,
        'password': None,
    },
    'refresh_time': 30,
    'display': {
        'type': None,
    }
}


class ConfigLoader:
    @classmethod
    def load(cls, path: str = 'config.yml'):
        config = dict(default_config)
        config.update(cls._load_file(path))
        config.update(cls._overwrite_config_with_env(config))
        return config

    @staticmethod
    def _load_file(path: str):
        if not os.path.exists(path):
            raise ConfigError(f"Configuration file {path} not found.")
        with open(path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    @classmethod
    def _overwrite_config_with_env(cls, config: dict, _path=None):
        path = _path or []
        env_key = '__'.join(path).upper()

        if isinstance(config, dict):
            for index, value in config.items():
                path.append(index)
                config[index] = cls._overwrite_config_with_env(value, path)
                del path[-1]
        elif os.environ.get(env_key):
            return os.environ.get(env_key)

        return config
