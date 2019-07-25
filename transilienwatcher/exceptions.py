class TransilienError(Exception):
    pass


class RequestError(TransilienError):
    pass


class FormatError(TransilienError):
    pass
