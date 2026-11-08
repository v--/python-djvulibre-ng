"""Functions for symbol S-expressions that hold unique string identifiers.

This is one of the four primary kinds of S-expressions.
"""
# mypy: disable-error-code=empty-body

import ctypes
from typing import Annotated

from djvulibre.ffi.ctypes_helpers import CType
from djvulibre.ffi.libdjvulibre import libdjvulibre
from djvulibre.ffi.miniexp.miniexp_t import MiniExpInternalKind

from .miniexp_t import miniexp_t


def miniexp_symbolp(p: miniexp_t) -> bool:
    """Test if a miniexp is a symbol expression.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a symbol expression.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.SYMBOL


@libdjvulibre.wrap_function
def miniexp_to_name(p: miniexp_t) -> Annotated[bytes | None, CType(ctypes.c_char_p)]:
    """Extract the value of a symbol miniexp.

    Args:
        p: Any miniexp.

    Returns:
        The value of `p` if it is a symbol miniexp and None otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_symbol(name: Annotated[bytes, CType(ctypes.c_char_p)]) -> miniexp_t:
    """Get the unique symbol miniexp with a given name.

    Args:
        name: Any string.

    Returns:
        A symbol miniexp.
    """
