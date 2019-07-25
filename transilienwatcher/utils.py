import os


def overwrite_config_with_env(config: dict, _path=None):
    path = _path or []
    env_key = '__'.join(path).upper()

    if isinstance(config, dict):
        for index, value in config.items():
            path.append(index)
            config[index] = overwrite_config_with_env(value, path)
            del path[-1]
    elif os.environ.get(env_key):
        return os.environ.get(env_key)

    return config
