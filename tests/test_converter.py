import pytest

from toolkit.converter import convert
from toolkit.errors import ConversionError


@pytest.mark.parametrize(
    "amount, source, target, result",
    [
        (1000, "mm", "m", 1.0),
        (1.5, "kg", "g", 1500.0),
        (0, "c", "f", 32.0),
        (-273.15, "c", "k", 0.0),
        (100, "c", "f", 212.0),
        (1, "km", "m", 1000.0),
    ],
)
def test_convert_positive(amount, source, target, result):
    assert convert(amount, source, target) == pytest.approx(result)


def test_absolute_zero_error():
    with pytest.raises(ConversionError):
        convert(-300, "c", "k")


def test_incompatible_units():
    with pytest.raises(ConversionError):
        convert(1, "kg", "m")


def test_unknown_unit():
    with pytest.raises(ConversionError):
        convert(1, "xyz", "m")


def test_uppercase_units():
    assert convert(0, "C", "F") == pytest.approx(32.0)
