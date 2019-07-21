#!/usr/bin/env python3
# coding: utf-8

import pytest

from rerwatcher import display
from tests.conftest import FAKE_CONFIG


class TestLCDDisplay:
    def test_print_on_matrix(self, mocker):
        lcd = mocker.patch('rerwatcher.display.CharLCD')
        messages = [mocker.Mock(**{'text.return_value': 'foo'})]
        matrix = display.LCDDisplay()

        matrix.print(messages)

        lcd().write_string.assert_called_once_with('foo')


class TestConsoleDisplay:
    def test_print_on_console(self, mocker):
        bi_print = mocker.patch('builtins.print')
        messages = [mocker.Mock(**{'text.return_value': 'foo'})]
        console = display.ConsoleDisplay()

        console.print(messages)

        bi_print.assert_called_with('foo')


class TestDisplayDeviceFactory:
    def test_device_builder_console_display(self):
        FAKE_CONFIG['device']['type'] = 'console'

        device = display.DisplayDeviceFactory.build(FAKE_CONFIG)

        assert isinstance(device, display.ConsoleDisplay)

    def test_device_builder_matrix_display(self, mocker):
        mocker.patch('rerwatcher.display.CharLCD')
        FAKE_CONFIG['device']['type'] = 'lcd'

        device = display.DisplayDeviceFactory.build(FAKE_CONFIG)

        assert isinstance(device, display.LCDDisplay)

    def test_device_builder_fail(self):
        FAKE_CONFIG['device']['type'] = 'foo'

        with pytest.raises(display.DisplayTypeNotSupportedError):
            display.DisplayDeviceFactory.build(FAKE_CONFIG)
