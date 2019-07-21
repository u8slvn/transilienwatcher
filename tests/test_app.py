#!/usr/bin/env python3
# coding: utf-8

import os

import pytest

from rerwatcher.app import RerWatcher


def test_rerwatcher_load_config(mocker):
    mocker.patch.dict(os.environ, {'API__URL': 'http://test.url'})

    config = RerWatcher.load_config()

    assert config['api']['url'] == 'http://test.url'
    assert config['device']['type'] == 'console'


def test_rerwatcher_workflow(mocker, mock_config, capsys):
    messages = [
        ['TEST: 1min', 'TEST: 1h'],
        ['TEST: 2min', 'TEST: 2h'],
    ]
    sleep = mocker.patch(
        'rerwatcher.app.time.sleep',
        side_effect=[True, KeyboardInterrupt]
    )
    fetch_data = mocker.patch(
        'rerwatcher.app.Transilien.fetch_data',
        side_effect=messages
    )

    app = RerWatcher(None)
    with pytest.raises(KeyboardInterrupt):
        app._app.start()

    expected = '\n'.join([m for msgs in messages for m in msgs]) + '\n'
    captured = capsys.readouterr()
    assert expected == captured.out
    assert 2 == fetch_data.call_count
    assert 2 == sleep.call_count
