# ruff: file-ignore[float-equality-comparison]

from . import floatnum as floatnum_miniexp
from . import number as number_miniexp
from . import string as string_miniexp


def test_miniexp_floatnum() -> None:
    expr = floatnum_miniexp.miniexp_floatnum(7.7)
    assert floatnum_miniexp.miniexp_floatnump(expr)
    assert floatnum_miniexp.miniexp_to_double(expr) == 7.7


def test_miniexp_floatnum_zero() -> None:
    # Ensure that no null pointer mess happens here.
    expr = floatnum_miniexp.miniexp_floatnum(0.0)
    assert floatnum_miniexp.miniexp_floatnump(expr)
    assert floatnum_miniexp.miniexp_to_double(expr) == 0.0


def test_miniexp_to_double_invalid() -> None:
    # Ensure that no null pointer mess happens here.
    expr = string_miniexp.miniexp_string(b'test')
    assert not floatnum_miniexp.miniexp_doublep(expr)
    assert floatnum_miniexp.miniexp_to_double(expr) == 0.0


def test_miniexp_to_double_integer() -> None:
    expr = number_miniexp.miniexp_number(3)
    assert not floatnum_miniexp.miniexp_floatnump(expr)
    assert floatnum_miniexp.miniexp_doublep(expr)
    assert floatnum_miniexp.miniexp_to_double(expr) == 3.0
