#!/usr/bin/env python3
# coding: utf-8

from abc import abstractmethod, ABC

from luma.core.interface.serial import spi, noop
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from luma.core.render import canvas
from luma.led_matrix.device import max7219


class DiplayTypeNotStupported(NotImplementedError):
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
        serial = spi(port=0, device=0, gpio=noop())
        self._device = max7219(
            serial, width=64, height=16, block_orientation=-90, rotate=0
        )
        self._device.contrast(32)

    def print(self, messages):
        with canvas(self._device) as draw:
            for message in messages:
                text(
                    draw, (0, 9), message.text(),
                    fill="white", font=proportional(LCD_FONT)
                )


class DisplayDeviceFactory(ABC):
    @staticmethod
    def build(config):
        type = config['device']['type']
        if type == 'matrix':
            return MatrixDisplay()
        if type == 'console':
            return ConsoleDisplay()

        raise DiplayTypeNotStupported
