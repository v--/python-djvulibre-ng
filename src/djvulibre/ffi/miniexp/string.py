"""Functions for floatnum S-expressions.

These are object S-expressions with a "string" class name.
"""
# mypy: disable-error-code=empty-body

import ctypes
import sys
from typing import Annotated

from djvulibre.ffi.ctypes_helpers import CType
from djvulibre.ffi.libdjvulibre import libdjvulibre

from .miniexp_t import miniexp_t


# Strings
@libdjvulibre.wrap_function
def miniexp_stringp(p: miniexp_t) -> bool:
    """Test if a miniexp is a string expression.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a string expression.
    """


# ctypes fails to convert to result to bytes correctly for some reason.
# The result of the miniexp_concat function produces gibberish when stringified, for example.
# This only affects GIL-enabled Python, however.
if (is_gil_enabled := getattr(sys, '_is_gil_enabled', None)) is None or is_gil_enabled():
    def miniexp_to_str(p: miniexp_t) -> bytes | None:
        c_string = ctypes.c_char_p()
        miniexp_to_lstr(p, ctypes.pointer(c_string))
        return c_string.value

    def miniexp_to_lstr(p: miniexp_t, sp: 'ctypes._Pointer[ctypes.c_char_p]') -> int:
        n = libdjvulibre.cdll.miniexp_to_lstr(p, sp)

        if value := sp.contents.value:
            sp.contents.value = value[:n]

        return n
else:
    @libdjvulibre.wrap_function
    def miniexp_to_str(p: miniexp_t) -> Annotated[bytes | None, CType(ctypes.c_char_p)]:
        """Extract the value of a string miniexp.

        Due to a memory alignment issue, a Python implementation is used when the GIL is enabled.

        Args:
            p: Any miniexp.

        Returns:
            The value of `p` if it is a string miniexp and None otherwise.
        """

    @libdjvulibre.wrap_function
    def miniexp_to_lstr(
        p: miniexp_t,
        sp: Annotated['ctypes._Pointer[ctypes.c_char_p]', CType(ctypes.POINTER(ctypes.c_char_p))],
    ) -> Annotated[int, CType(ctypes.c_int)]:
        """Get the length and value of a string miniexp.

        Due to a memory alignment issue, a Python implementation is used when the GIL is enabled.

        Args:
            p: Any miniexp.
            sp: A pointer to a C string to assign the value of `p` to. It will be assigned the null pointer if `p` is not a string miniexp.

        Returns:
            The length of `p` if it is a string miniexp and 0 otherwise.
        """


@libdjvulibre.wrap_function
def miniexp_string(p: Annotated[bytes, CType(ctypes.c_char_p)]) -> miniexp_t:
    """Construct a string expression from a string.

    Args:
        p: The string to use.

    Returns:
        A string miniexp.
    """


@libdjvulibre.wrap_function
# ruff: ignore[builtin-argument-shadowing]
def miniexp_lstring(len: Annotated[int, CType(ctypes.c_size_t)], p: Annotated[bytes, CType(ctypes.c_char_p)]) -> miniexp_t:
    """Construct a miniexp by copying the first n bytes of a string.

    The same as miniexp_substring from the perspective of the Python FFI.

    Args:
        len: The number of bytes.
        p: The byte encoding of a string.

    Returns:
        A string miniexp.
    """


@libdjvulibre.wrap_function
# ruff: ignore[builtin-argument-shadowing]
def miniexp_substring(p: Annotated[bytes, CType(ctypes.c_char_p)], len: Annotated[int, CType(ctypes.c_size_t)]) -> miniexp_t:
    """Construct a miniexp by copying at most n bytes of a string.

    The same as miniexp_lstring from the perspective of the Python FFI.

    Args:
        len: The number of bytes.
        p: The byte encoding of a string.

    Returns:
        A string miniexp.
    """


@libdjvulibre.wrap_function
def miniexp_concat(l: miniexp_t) -> miniexp_t:
    """Concatenate all direct string subexpressions in a list into a single string miniexp.

    Args:
        l: The list miniexp to concatenate.

    Returns:
        The concatenated string. If the argument is a cyclic list, return the empty list.
    """
