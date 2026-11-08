"""Functions for floatnum S-expressions.

These are object S-expressions with a "floatnum" class name.
"""
# mypy: disable-error-code=empty-body

import ctypes
from typing import Annotated

from djvulibre.ffi.ctypes_helpers import CType
from djvulibre.ffi.libdjvulibre import libdjvulibre

from .miniexp_t import miniexp_t


@libdjvulibre.wrap_function
def miniexp_floatnump(p: miniexp_t) -> bool:
    """Test if a miniexp is a floatnum expression.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a floatnum expression.
    """


@libdjvulibre.wrap_function
def miniexp_floatnum(x: Annotated[float, CType(ctypes.c_double)]) -> miniexp_t:
    """Construct a floatnum miniexp.

    Args:
        x: Any double-precision floating-point number.

    Returns:
        A floatnum miniexp.
    """


@libdjvulibre.wrap_function
def miniexp_doublep(p: miniexp_t) -> bool:
    """Test if a miniexp encodes a a double-precision floating-point number.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a floatnum or number miniexp.
    """


@libdjvulibre.wrap_function
def miniexp_to_double(p: miniexp_t) -> Annotated[float, CType(ctypes.c_double)]:
    """Get the value of a floatnum or number miniexp.

    Args:
        p: Any miniexp.

    Returns:
        A double-precision floating-point number if `p` is a floatnum and 0.0 otherwise.
    """
