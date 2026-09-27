import pytest

from toolkit.calculator import calculate
from toolkit.errors import CalculationError


# Позитивные тесты
@pytest.mark.parametrize("expression, result", [
    ("2+3*4", 14),
    ("10 / 4", 2.5),
    ("-2 * -3", 6),
    ("1+-2", -1),
    ("(2+3)*4", 20),
])
def test_calculate_positive(expression, result):
    assert calculate(expression) == result


# Негативные тесты
@pytest.mark.parametrize("expression", [
    "",
    "2+a",
    "2*/3",
    "(2+3",
])
def test_calculate_errors(expression):
    with pytest.raises(CalculationError):
        calculate(expression)


# Унарные знаки
@pytest.mark.parametrize("expression, result", [
    ("--2", 2),
    ("+-2", -2),
    ("---2", -2),
    ("2--2", 4),
    ("2+-2", 0),
])
def test_unary_signs(expression, result):
    assert calculate(expression) == result


# Деление на ноль
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("1/0")