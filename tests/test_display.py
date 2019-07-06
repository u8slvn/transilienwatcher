#!/usr/bin/env python3
# coding: utf-8

from unittest.mock import patch, Mock

import pytest

from rerwatcher import display
from tests.conftest import FAKE_CONFIG


class TestConsoleDisplay:
    @patch('builtins.print')
    def test_print_on_console(self, print):
        message = Mock()
        message.text.return_value = 'FOO'
        messages = [message]
        console_display = display.ConsoleDisplay()

        console_display.print(messages)

        print.assert_called_with('FOO')


class TestDisplayDeviceFactory:
    @patch('rerwatcher.display.ConsoleDisplay')
    def test_device_builder_console_display(self, console_display):
        FAKE_CONFIG['device']['type'] = 'console'
        console_display.return_value = 'FOO-CONSOLE'

        device = display.DisplayDeviceFactory.build(FAKE_CONFIG)

        assert device == 'FOO-CONSOLE'

    @patch('rerwatcher.display.MatrixDisplay')
    def test_device_builder_matrix_display(self, matrix_display):
        FAKE_CONFIG['device']['type'] = 'matrix'
        matrix_display.return_value = 'FOO-MATRIX'

        device = display.DisplayDeviceFactory.build(FAKE_CONFIG)

        assert device == 'FOO-MATRIX'

    def test_device_builder_fail(self):
        FAKE_CONFIG['device']['type'] = 'foo'

        with pytest.raises(display.DiplayTypeNotStupported) as error:
            display.DisplayDeviceFactory.build(FAKE_CONFIG)

        assert error.typename == 'DiplayTypeNotStupported'
