"""Functions for integer ("number") S-expressions.

This is one of the four primary kinds of S-expressions. Floating point ("floatnum") expressions are instead considered objects.
"""
# mypy: disable-error-code=empty-body

import sys

from .miniexp_t import MiniExpInternalKind, miniexp_t


def miniexp_numberp(p: miniexp_t) -> bool:
    """Test if a miniexp is a number expression.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a number expression.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.NUMBER


def miniexp_to_int(p: miniexp_t) -> int:
    """Extract the integer value of a number miniexp.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        The value of `p` if it is a number miniexp and gibberish otherwise.
    """
    return p.address >> 2


def miniexp_number(x: int) -> miniexp_t:
    """Construct a number miniexp from an integer.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        x: Any integer.

    Returns:
        A number miniexp.
    """
    if x > sys.maxsize:
        raise OverflowError(f'The integer {x} is too large')

    return miniexp_t(x << 2 | 3)
