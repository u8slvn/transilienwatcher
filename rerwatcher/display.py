from abc import abstractmethod, ABC

from RPLCD import CharLCD


class UnknownDisplayTypeError(NotImplementedError):
    pass


class Display(ABC):
    @abstractmethod
    def print(self, messages):
        raise NotImplementedError


class Console(Display):
    def print(self, messages):
        for message in messages:
            print(message)


class LCD(Display):
    def __init__(self):
        self._device = CharLCD('PCF8574', 0x27)

    def print(self, messages):
        for line, message in enumerate(messages, 1):
            self._device.cursor_pos = (line, 0)
            self._device.write_string(message)


class DisplayBuilder(ABC):
    @staticmethod
    def build(config: dict):
        display = {
            'lcd': LCD,
            'console': Console,
        }.get(config['type'])

        if not display:
            raise UnknownDisplayTypeError

        return display()
