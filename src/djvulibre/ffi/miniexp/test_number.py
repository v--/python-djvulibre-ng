import pytest

from . import number as number_miniexp


def test_miniexp_number() -> None:
    expr = number_miniexp.miniexp_number(7)
    assert number_miniexp.miniexp_numberp(expr)
    assert number_miniexp.miniexp_to_int(expr) == 7


def test_miniexp_number_zero() -> None:
    # Ensure that no null pointer mess happens here.
    expr = number_miniexp.miniexp_number(0)
    assert number_miniexp.miniexp_numberp(expr)
    assert number_miniexp.miniexp_to_int(expr) == 0


def test_miniexp_number_large() -> None:
    with pytest.raises(OverflowError):
        number_miniexp.miniexp_number(2 ** 64)
