class ToolkitError(Exception):
    """Базовый класс для всех ошибок пакета toolkit."""


class CalculationError(ToolkitError):
    """Ошибка при вычислении арифметического выражения."""


class ConversionError(ToolkitError):
    """Ошибка при конвертации величин."""


class CLIError(ToolkitError):
    """Ошибка при разборе аргументов командной строки."""