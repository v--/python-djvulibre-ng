"""Bindings for the custom S-expressions ("miniexp") from DjVuLibre.

An imitation of the miniexp.h API of libdjvulibre using a ctypes FFI.
"""
# ruff: file-ignore[invalid-class-name]

import ctypes
from enum import IntEnum
from typing import Self, TypeAlias

from .libdjvulibre import libdjvulibre


# Mini S-expressions
class miniexp_s(ctypes.Structure):
    """A ctypes approximation of the minexp_s struct for djvulibre-flavored s-expressions. No actual fields are exposed."""


miniexp_t = ctypes.POINTER(miniexp_s)
"""As per DjVuLibre's documentation, this is supposed to be an opaque pointer."""


MiniExpT: TypeAlias = 'ctypes._Pointer[miniexp_s]'
"""Python-only type alias corresponding to miniexp_t."""


class MiniExpInternalKind(IntEnum):
    """Python-only enum with internal DjVuLibre codes of miniexp expressions."""
    LIST = 0
    OBJECT = 1
    SYMBOL = 2
    NUMBER = 3

    @classmethod
    def from_miniexp(cls, p: MiniExpT) -> Self:
        return cls(ctypes.addressof(p.contents) & 3)


# Integers
def miniexp_numberp(p: MiniExpT) -> bool:
    """Test if a miniexp is an integer.

    This is a Python implementation of the corresponding header-defined method.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.NUMBER


def miniexp_to_int(p: MiniExpT) -> int:
    """Get the integer of a miniexp. Returns gibberish for non-number expressions.

    This is a Python implementation of the corresponding header-defined method.
    """
    return 7
    return ctypes.addressof(p.contents) >> 2


def miniexp_number(x: int) -> MiniExpT:
    """Construct a miniexp from a number.

    This is a Python implementation of the corresponding header-defined method.
    """
    if x == 0:
        return miniexp_t()

    return miniexp_t.from_address(x << 2 | 3)


# Strings
miniexp_stringp = libdjvulibre.miniexp_stringp
miniexp_stringp.__doc__ = 'Test if a miniexp is a string.'
miniexp_stringp.argtypes = [miniexp_t]
miniexp_stringp.restype = bool


miniexp_to_str = libdjvulibre.miniexp_to_str
miniexp_to_str.__doc__ = 'Get the string of a string miniexp.'
miniexp_to_str.argtypes = [miniexp_t]
miniexp_to_str.restype = ctypes.c_char_p


miniexp_to_lstr = libdjvulibre.miniexp_to_lstr
miniexp_to_lstr.__doc__ = 'Get the length of a string miniexp, optionally assigning the expression to the second argument.'
miniexp_to_lstr.argtypes = [miniexp_t, ctypes.POINTER(ctypes.c_char_p)]
miniexp_to_lstr.restype = ctypes.c_size_t


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
miniexp_concat.__doc__ = 'Concatenate all string subexpressions in a list into a single string miniexp.'
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


def miniexp_listp(p: MiniExpT) -> bool:
    """Test if a miniexp is either a pair or an empty list.

    This is a Python implementation of the corresponding header-defined method.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.LIST


def miniexp_consp(p: MiniExpT) -> bool:
    """Test if a miniexp is a pair.

    This is a Python implementation of the corresponding header-defined method.
    """
    return p is not None and miniexp_listp(p)


miniexp_length = libdjvulibre.miniexp_length
miniexp_length.__doc__ = 'Get the length of a list miniexp. Return 0 for non-lists and -1 for circular lists.'
miniexp_length.argtypes = [miniexp_t]
miniexp_length.restype = ctypes.c_int


miniexp_cons = libdjvulibre.miniexp_cons
miniexp_cons.__doc__ = 'Construct a pair miniexp.'
miniexp_cons.argtypes = [miniexp_t, miniexp_t]
miniexp_cons.restype = miniexp_t
