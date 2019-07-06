#!/usr/bin/env python3
# coding: utf-8

import os

import yaml

from .api import TransilienApi
from .app import RerWatcher
from .display import DisplayDeviceFactory


def load_config():
    """Load RerWatcher configuration

    Load the default configuration from 'config.yml' file and check for
    each parameters from each sections if no environment variables is
    set. If it does, the default yaml value is overwrite by the
    environment's one.

    Returns:
        config (dict): the global rerwatcher configuration

    """
    with open('config.yml', 'r') as ymlconf:
        config = yaml.load(ymlconf, Loader=yaml.FullLoader)

    for section in config:
        for param in config[section]:
            env_key = "{section}_{param}".format(
                section=section,
                param=param,
            ).upper()
            default_value = config[section][param]

            config[section][param] = os.environ.get(env_key, default_value)

    return config


def build_rer_watcher():
    """RERWatcher builder

    Build and bootsrap the RERWatcher application.

    Returns:
        app (RerWatcher): the application instance

    """
    config = load_config()

    matrix_display = DisplayDeviceFactory.build(config)
    transilien_api = TransilienApi(config)

    app = RerWatcher(
        config=config,
        display=matrix_display,
        api=transilien_api
    )

    return app
