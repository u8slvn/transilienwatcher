from abc import abstractmethod, ABC

from RPLCD import CharLCD


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


class LCDDisplay(DisplayDevice):
    def __init__(self):
        self._device = CharLCD('PCF8574', 0x27)

    def print(self, messages):
        for line, message in enumerate(messages, 1):
            self._device.cursor_pos = (line, 0)
            self._device.write_string(message.text())


class DisplayDeviceFactory(ABC):
    @staticmethod
    def build(config: dict):
        display = {
            'lcd': LCDDisplay,
            'console': ConsoleDisplay,
        }.get(config['device']['type'])

        if not display:
            raise DisplayTypeNotSupportedError

        return display()
