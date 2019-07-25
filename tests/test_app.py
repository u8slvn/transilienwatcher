#!/usr/bin/env python3
# coding: utf-8

import os

import pytest

from transilienwatcher.app import TransilienWatcher


def test_rerwatcher_load_config(mocker):
    mocker.patch.dict(os.environ, {'TRANSILIEN__URL': 'http://test.url'})

    config = TransilienWatcher.load_config()

    assert config['transilien']['url'] == 'http://test.url'
    assert config['display']['type'] == 'console'


def test_rerwatcher_workflow(mocker, mock_config, capsys):
    messages = [
        ['TEST: 1min', 'TEST: 1h'],
        ['TEST: 2min', 'TEST: 2h'],
    ]
    sleep = mocker.patch(
        'transilienwatcher.app.time.sleep',
        side_effect=[True, KeyboardInterrupt]
    )
    fetch_data = mocker.patch(
        'transilienwatcher.app.Transilien.fetch_data',
        side_effect=messages
    )

    app = TransilienWatcher(None)
    with pytest.raises(KeyboardInterrupt):
        app.run()

    expected = '\n'.join([m for msgs in messages for m in msgs]) + '\n'
    captured = capsys.readouterr()
    assert expected == captured.out
    assert 2 == fetch_data.call_count
    assert 2 == sleep.call_count
