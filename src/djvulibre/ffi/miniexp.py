"""Bindings for the custom S-expressions ("miniexp") from DjVuLibre.

An imitation of the miniexp.h API of libdjvulibre using a ctypes FFI.
"""
# ruff: file-ignore[invalid-class-name]

import ctypes
import sys
from enum import IntEnum
from typing import Self

from .libdjvulibre import libdjvulibre


class miniexp_t(ctypes.c_void_p):
    """An opaque pointer to a miniexp."""

    @property
    def address(self) -> int:
        return self.value or 0

    @property
    def is_null(self) -> bool:
        return self.value is None

    def __hash__(self) -> int:
        return self.address

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ctypes.c_void_p):
            return self.address == (other.value or 0)

        if isinstance(other, int):
            return self.address == other

        return False


class MiniExpInternalKind(IntEnum):
    """Python-only enum with internal DjVuLibre codes of miniexp expressions."""
    LIST = 0
    OBJECT = 1
    SYMBOL = 2
    NUMBER = 3

    @classmethod
    def from_miniexp(cls, p: miniexp_t) -> Self:
        return cls(p.address & 3)


# Integers
def miniexp_numberp(p: miniexp_t) -> bool:
    """Test if a miniexp is an integer.

    This is a Python implementation of the corresponding header-defined function.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.NUMBER


def miniexp_to_int(p: miniexp_t) -> int:
    """Get the integer of a miniexp. Returns gibberish for non-number expressions.

    This is a Python implementation of the corresponding header-defined function.
    """
    return p.address >> 2


def miniexp_number(x: int) -> miniexp_t:
    """Construct a miniexp from a number.

    This is a Python implementation of the corresponding header-defined function.
    """
    if x > sys.maxsize:
        raise OverflowError(f'The integer {x} is too large')

    return miniexp_t(x << 2 | 3)


# Strings
miniexp_stringp = libdjvulibre.miniexp_stringp
miniexp_stringp.__doc__ = 'Test if a miniexp is a string.'
miniexp_stringp.argtypes = [miniexp_t]
miniexp_stringp.restype = bool


def miniexp_to_str(p: miniexp_t) -> bytes | None:
    """Get the string of a string miniexp.

    This is a Python reimplementation of the corresponding C function, which ctypes does not wrap correctly.
    """
    c_string = ctypes.c_char_p()
    miniexp_to_lstr(p, ctypes.pointer(c_string))
    return c_string.value


def miniexp_to_lstr(p: miniexp_t, sp: 'ctypes._Pointer[ctypes.c_char_p]') -> int | None:
    """Get the length of a string miniexp, optionally assigning the expression to the second argument. Assigns the empty list of the argument is not a string miniexp."""
    n = libdjvulibre.miniexp_to_lstr(p, sp)

    # ctypes fails to wrap the conversion to bytes correctly for some reason.
    # The result of the miniexp_concat function produces gibberish when stringified, for example.
    if value := sp.contents.value:
        sp.contents.value = value[:n]

    return n


miniexp_string = libdjvulibre.miniexp_string
miniexp_string.__doc__ = 'Construct a miniexp from a string.'
miniexp_string.argtypes = [ctypes.c_char_p]
miniexp_string.restype = miniexp_t


miniexp_lstring = libdjvulibre.miniexp_lstring
miniexp_lstring.__doc__ = 'Construct a miniexp by copying the first n bytes of a string.\nThe same as miniexp_substring from the perspective of the Python FFI.'
miniexp_lstring.argtypes = [ctypes.c_size_t, ctypes.c_char_p]
miniexp_lstring.restype = miniexp_t


miniexp_substring = libdjvulibre.miniexp_substring
miniexp_substring.__doc__ = 'Construct a miniexp by copying at most n bytes of a string.'
miniexp_substring.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
miniexp_substring.restype = miniexp_t


miniexp_concat = libdjvulibre.miniexp_concat
miniexp_concat.__doc__ = 'Concatenate all direct string subexpressions in a list into a single string miniexp. If the argument is a cyclic list, return the empty list.'
miniexp_concat.argtypes = [miniexp_t]
miniexp_concat.restype = miniexp_t


# Lists
miniexp_nil = miniexp_t()
"""An empty miniexp list.

This is a Python implementation of the corresponding header-defined value.
"""


miniexp_dummy = miniexp_t.from_address(2)
"""An invalid expression used to represent various exceptional conditions.

This is a Python implementation of the corresponding header-defined value.
"""


def miniexp_listp(p: miniexp_t) -> bool:
    """Test if a miniexp is either a pair or an empty list.

    This is a Python implementation of the corresponding header-defined function.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.LIST


def miniexp_consp(p: miniexp_t) -> bool:
    """Test if a miniexp is a pair.

    This is a Python implementation of the corresponding header-defined function.
    """
    return not p.is_null and miniexp_listp(p)


miniexp_length = libdjvulibre.miniexp_length
miniexp_length.__doc__ = 'Get the length of a list miniexp. Return 0 for non-lists and -1 for circular lists.'
miniexp_length.argtypes = [miniexp_t]
miniexp_length.restype = ctypes.c_int


def miniexp_car(p: miniexp_t) -> miniexp_t:
    """Get the first value of a pair. If the argument is not a pair, return the empty list.

    This is a Python implementation of the corresponding header-defined function.
    """
    if miniexp_consp(p):
        return miniexp_t.from_address(p.address)

    return miniexp_nil


def miniexp_cdr(p: miniexp_t) -> miniexp_t:
    """Get the second value of a pair. If the argument is not a pair, return the empty list.

    This is a Python implementation of the corresponding header-defined function.
    """
    if miniexp_consp(p):
        return miniexp_t.from_address(p.address + ctypes.alignment(ctypes.c_void_p))

    return miniexp_nil


miniexp_caar = libdjvulibre.miniexp_caar
miniexp_caar.__doc__ = 'Get the first value of the first value of a pair.'
miniexp_caar.argtypes = [miniexp_t]
miniexp_caar.restype = miniexp_t


miniexp_cdar = libdjvulibre.miniexp_cdar
miniexp_cdar.__doc__ = 'Get the second value of the first value of a pair.'
miniexp_cdar.argtypes = [miniexp_t]
miniexp_cdar.restype = miniexp_t


miniexp_cadr = libdjvulibre.miniexp_cadr
miniexp_cadr.__doc__ = 'Get the first value of the second value of a pair.'
miniexp_cadr.argtypes = [miniexp_t]
miniexp_cadr.restype = miniexp_t


miniexp_cddr = libdjvulibre.miniexp_cddr
miniexp_cddr.__doc__ = 'Get the second value of the second value of a pair.'
miniexp_cddr.argtypes = [miniexp_t]
miniexp_cddr.restype = miniexp_t


miniexp_caddr = libdjvulibre.miniexp_caddr
miniexp_caddr.__doc__ = 'Get the first value of the second value of the second value of a pair.'
miniexp_caddr.argtypes = [miniexp_t]
miniexp_caddr.restype = miniexp_t


miniexp_cdddr = libdjvulibre.miniexp_cdddr
miniexp_cdddr.__doc__ = 'Get the second value of second value of the second value of a pair.'
miniexp_cdddr.argtypes = [miniexp_t]
miniexp_cdddr.restype = miniexp_t


miniexp_nth = libdjvulibre.miniexp_nth
miniexp_nth.__doc__ = 'Get the n-th element of a list.'
miniexp_nth.argtypes = [ctypes.c_int, miniexp_t]
miniexp_nth.restype = miniexp_t


miniexp_cons = libdjvulibre.miniexp_cons
miniexp_cons.__doc__ = 'Construct a pair miniexp.'
miniexp_cons.argtypes = [miniexp_t, miniexp_t]
miniexp_cons.restype = miniexp_t


miniexp_rplaca = libdjvulibre.miniexp_rplaca
miniexp_rplaca.__doc__ = 'Replace the first value of a pair and return the new first value. If the argument is not a list, simply return the empty list.'
miniexp_rplaca.argtypes = [miniexp_t, miniexp_t]
miniexp_rplaca.restype = miniexp_t


miniexp_rplacd = libdjvulibre.miniexp_rplacd
miniexp_rplacd.__doc__ = 'Replace the second value of a pair and return the new second value. If the argument is not a list, simply return the empty list.'
miniexp_rplacd.argtypes = [miniexp_t, miniexp_t]
miniexp_rplacd.restype = miniexp_t


miniexp_reverse = libdjvulibre.miniexp_reverse
miniexp_reverse.__doc__ = 'Reverse a list in-place. If the argument is not a list, simply return the empty list.'
miniexp_reverse.argtypes = [miniexp_t]
miniexp_reverse.restype = miniexp_t
