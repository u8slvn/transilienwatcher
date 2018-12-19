#!/usr/bin/env python3
# coding: utf-8

from unittest.mock import patch, Mock

import pytest

from rerwatcher.app import RerWatcher


class TestRerWatcher:
    @patch('rerwatcher.app.time.sleep', side_effect=KeyboardInterrupt)
    def test_rerwatcher_workflow(self, sleep, fake_config):
        app = RerWatcher(config=fake_config, display=Mock(), api=Mock())
        with pytest.raises(KeyboardInterrupt):
            app.start()

        assert app._api.fetch_data.called
        assert app._display.print.called
        assert sleep.called
