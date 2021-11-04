class TransilienError(Exception):
    pass


class RequestError(TransilienError):
    pass


class FormatError(TransilienError):
    pass


class ConfigError(Exception):
    pass


class InvalidConfigError(ConfigError):
    pass


class ConfigNotFoundError(ConfigError):
    pass
