#!/usr/bin/env python3
# coding: utf-8

from abc import abstractmethod, ABC

from luma.core.interface import serial
from luma.core.legacy import text, font
from luma.core.render import canvas
from luma.led_matrix import device


class DisplayTypeNotSupportedError(NotImplementedError):
    pass


class DisplayDevice(ABC):
    @abstractmethod
    def print(self, messages):
        pass


class ConsoleDisplay(DisplayDevice):
    def print(self, messages):
        for message in messages:
            print(message.text())


class MatrixDisplay(DisplayDevice):
    def __init__(self):
        _serial = serial.spi(port=0, device=0, gpio=serial.noop())
        self._device = device.max7219(
            _serial, width=64, height=16, block_orientation=-90, rotate=0
        )
        self._device.contrast(32)

    def print(self, messages):
        with canvas(self._device) as draw:
            for message in messages:
                text(
                    draw, (0, 9), message.text(),
                    fill="white", font=font.proportional(font.LCD_FONT)
                )


class DisplayDeviceFactory(ABC):
    @staticmethod
    def build(config: dict):
        display = {
            'matrix': MatrixDisplay,
            'console': ConsoleDisplay,
        }.get(config['device']['type'])

        if not display:
            raise DisplayTypeNotSupportedError

        return display()
