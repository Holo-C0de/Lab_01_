import json
from pathlib import Path

from .errors import ConversionError

CONFIG_PATH = Path(__file__).parent / "conversions.json"
with open(CONFIG_PATH, encoding="utf-8") as f:  # Загрузка конфига
    CONFIG = json.load(f)
UNIT_GROUPS = {}  # Соответствие единицы и группы
for (
    group_name,
    group_data,
) in (
    CONFIG.items()
):  # В group_name будет "length" или "mass"; В group_data будет словарь с base и units.
    for unit in group_data["units"]:  # В unit будет "mm", "cm", "m", "km", "g", "kg"
        UNIT_GROUPS[unit] = group_name

for unit in ("c", "f", "k"):  # Присваивание типа "температура"
    UNIT_GROUPS[unit] = "temperature"


def convert(amount: float, source_unit: str, target_unit: str) -> float:
    """
    Переводит значение из одной единицы измерения в другую.

    Поддерживает три группы единиц: длина, масса и температура.
    Регистр единиц не учитывается. Перевод между разными группами
    запрещён. Для температуры дополнительно проверяется абсолютный
    ноль.

    Args:
        amount: Числовое значение для перевода.
        source_unit: Исходная единица измерения.
        target_unit: Целевая единица измерения.

    Returns:
        Результат перевода в виде числа.

    Raises:
        ConversionError: Если единица неизвестна, единицы относятся
            к разным группам, или температура ниже абсолютного нуля.
    """
    source_unit = source_unit.lower()
    target_unit = target_unit.lower()
    if source_unit not in UNIT_GROUPS:
        raise ConversionError(f"Неизвестная единица: {source_unit}")

    if target_unit not in UNIT_GROUPS:
        raise ConversionError(f"Неизвестная единица: {target_unit}")

    # Блок проверка совпадения групп
    source_group = UNIT_GROUPS[
        source_unit
    ]  # Сохраняем группу исходной единицы в переменную.
    if source_group != UNIT_GROUPS[target_unit]:
        raise ConversionError(f"Несовместимые единицы: {source_unit} и {target_unit}")

    # Блок конвертация температуры
    elif source_group == "temperature":
        return _convert_temperature(
            temp_amount=amount,
            source_temp=source_unit,
            target_temp=target_unit,
        )  # Передача в функцию температуры: значение, откуда и куда

    # Блок конвертация длины и массы
    else:
        unit_coefficients = CONFIG[
            source_group
        ][
            "units"
        ]  # CONFIG — словарь из conversions.json, CONFIG[source_group] — данные группы, ["units"] — берём только вложенный словарь с коэффициентами.

        # Переводим в базовую единицу группы (например, mm -> m)
        amount_in_base = (
            amount * unit_coefficients[source_unit]
        )  # unit_coefficients[source_unit] — коэффициент исходной единицы относительно базовой.

        # Переводим из базовой в целевую (например, m -> km)
        converted_amount = amount_in_base / unit_coefficients[target_unit]
        return float(converted_amount)


def _convert_temperature(
    temp_amount: float, source_temp: str, target_temp: str
) -> float:
    """
    Переводит значение температуры между Цельсием, Фаренгейтом
    и Кельвином.

    Сначала приводит исходное значение к Цельсию, проверяет, что
    температура не ниже абсолютного нуля, затем переводит из Цельсия
    в целевую шкалу.

    Args:
        temp_amount: Числовое значение температуры для перевода.
        source_temp: Исходная шкала: ``"c"``, ``"f"`` или ``"k"``.
        target_temp: Целевая шкала: ``"c"``, ``"f"`` или ``"k"``.

    Returns:
        Результат перевода в виде числа.

    Raises:
        ConversionError: Если температура ниже абсолютного нуля (меньше -273.15 °C).
    """

    # Переводим исходное значение в Цельсий
    if source_temp == "c":
        celsius = temp_amount
    elif source_temp == "f":
        celsius = (temp_amount - 32) * 5 / 9
    elif source_temp == "k":
        celsius = temp_amount - 273.15

    # Проверка абсолютного нуля
    if celsius < -273.15:
        raise ConversionError("Температура ниже абсолютного нуля")

    # Переводим из Цельсия в целевую шкалу
    if target_temp == "c":
        result = celsius
    elif target_temp == "f":
        result = celsius * 9 / 5 + 32
    elif target_temp == "k":
        result = celsius + 273.15

    return float(result)
