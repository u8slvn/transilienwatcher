from abc import abstractmethod, ABC

from RPLCD import CharLCD


class DisplayTypeNotSupportedError(NotImplementedError):
    pass


class DisplayDevice(ABC):
    @abstractmethod
    def print(self, messages):
        raise NotImplementedError


class Console(DisplayDevice):
    def print(self, messages):
        for message in messages:
            print(message)


class LCD(DisplayDevice):
    def __init__(self):
        self._device = CharLCD('PCF8574', 0x27)

    def print(self, messages):
        for line, message in enumerate(messages, 1):
            self._device.cursor_pos = (line, 0)
            self._device.write_string(message)


class DisplayDeviceFactory(ABC):
    @staticmethod
    def build(config: dict):
        display = {
            'lcd': LCD,
            'console': Console,
        }.get(config['type'])

        if not display:
            raise DisplayTypeNotSupportedError

        return display()
