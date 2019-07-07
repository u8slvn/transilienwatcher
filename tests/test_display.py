#!/usr/bin/env python3
# coding: utf-8

import pytest

from rerwatcher import display
from tests.conftest import FAKE_CONFIG


class TestMatrixDisplay:
    def test_print_on_matrix(self, mocker, mock_luma):
        messages = [mocker.Mock(**{'text.return_value': 'foo'})]
        matrix = display.MatrixDisplay()
        *_, text, _, canvas = mock_luma

        matrix.print(messages)

        canvas.assert_called_once()
        text.assert_called_once()


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

    def test_device_builder_matrix_display(self, mock_luma):
        FAKE_CONFIG['device']['type'] = 'matrix'

        device = display.DisplayDeviceFactory.build(FAKE_CONFIG)

        assert isinstance(device, display.MatrixDisplay)

    def test_device_builder_fail(self):
        FAKE_CONFIG['device']['type'] = 'foo'

        with pytest.raises(display.DisplayTypeNotSupportedError):
            display.DisplayDeviceFactory.build(FAKE_CONFIG)
