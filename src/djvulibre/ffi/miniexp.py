"""Bindings for the custom S-expressions ("miniexp") from DjVuLibre.

An recreation of the miniexp.h API of libdjvulibre using a ctypes FFI.
"""
# ruff: file-ignore[invalid-class-name]
# mypy: disable-error-code=empty-body

import ctypes
import sys
from enum import IntEnum
from typing import TYPE_CHECKING, Self

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
    """Construct a miniexp from an integer.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        x: Any integer.

    Returns:
        A number miniexp.
    """
    if x > sys.maxsize:
        raise OverflowError(f'The integer {x} is too large')

    return miniexp_t(x << 2 | 3)


# Symbols
def miniexp_symbolp(p: miniexp_t) -> bool:
    """Test if a miniexp is a symbol expression.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a symbol expression.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.SYMBOL


if not TYPE_CHECKING:
    miniexp_to_name = libdjvulibre.cdll.miniexp_to_name
    miniexp_to_name.argtypes = [miniexp_t]
    miniexp_to_name.restype = ctypes.c_char_p
else:
    def miniexp_to_name(p: miniexp_t) -> bytes | None:
        """Extract the value of a symbol miniexp.

        Args:
            p: Any miniexp.

        Returns:
            The value of `p` if it is a symbol miniexp and None otherwise.
        """


if not TYPE_CHECKING:
    miniexp_symbol = libdjvulibre.cdll.miniexp_symbol
    miniexp_symbol.argtypes = [ctypes.c_char_p]
    miniexp_symbol.restype = miniexp_t
else:
    def miniexp_symbol(name: bytes) -> miniexp_t:
        """Get the unique symbol miniexp with a given name.

        Args:
            name: Any string.

        Returns:
            A symbol miniexp.
        """


# Strings
if not TYPE_CHECKING:
    miniexp_stringp = libdjvulibre.cdll.miniexp_stringp
    miniexp_stringp.argtypes = [miniexp_t]
    miniexp_stringp.restype = bool
else:
    def miniexp_stringp(p: miniexp_t) -> bool:
        """Test if a miniexp is a string expression.

        Args:
            p: Any miniexp.

        Returns:
            Whether `p` is a string expression.
        """


if not TYPE_CHECKING:
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
        miniexp_to_str = libdjvulibre.cdll.miniexp_to_str
        miniexp_to_str.argtypes = [miniexp_t]
        miniexp_to_str.restype = ctypes.c_char_p

        miniexp_to_lstr = libdjvulibre.cdll.miniexp_to_lstr
        miniexp_to_lstr.argtypes = [miniexp_t, ctypes.POINTER(ctypes.c_char_p)]
        miniexp_to_lstr.restype = ctypes.c_int
else:
    def miniexp_to_str(p: miniexp_t) -> bytes | None:
        """Extract the value of a string miniexp.

        Due to a memory alignment issue, a Python implementation is used when the GIL is enabled.

        Args:
            p: Any miniexp.

        Returns:
            The value of `p` if it is a string miniexp and None otherwise.
        """

    def miniexp_to_lstr(p: miniexp_t, sp: 'ctypes._Pointer[ctypes.c_char_p]') -> int:
        """Get the length and value of a string miniexp.

        Due to a memory alignment issue, a Python implementation is used when the GIL is enabled.

        Args:
            p: Any miniexp.
            sp: A pointer to a C string to assign the value of `p` to. It will be assigned the null pointer if `p` is not a string miniexp.

        Returns:
            The length of `p` if it is a string miniexp and 0 otherwise.
        """


if not TYPE_CHECKING:
    miniexp_string = libdjvulibre.cdll.miniexp_string
    miniexp_string.argtypes = [ctypes.c_char_p]
    miniexp_string.restype = miniexp_t
else:
    def miniexp_string(p: bytes) -> miniexp_t:
        """Construct a string expression from a string.

        Args:
            p: The string to use.

        Returns:
            A string miniexp.
        """


if not TYPE_CHECKING:
    miniexp_lstring = libdjvulibre.cdll.miniexp_lstring
    miniexp_lstring.argtypes = [ctypes.c_size_t, ctypes.c_char_p]
    miniexp_lstring.restype = miniexp_t
else:
    # ruff: ignore[builtin-argument-shadowing]
    def miniexp_lstring(len: int, p: bytes) -> miniexp_t:
        """Construct a miniexp by copying the first n bytes of a string.

        The same as miniexp_substring from the perspective of the Python FFI.

        Args:
            len: The number of bytes.
            p: The byte encoding of a string.

        Returns:
            A string miniexp.
        """


if not TYPE_CHECKING:
    miniexp_substring = libdjvulibre.cdll.miniexp_substring
    miniexp_substring.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
    miniexp_substring.restype = miniexp_t
else:
    # ruff: ignore[builtin-argument-shadowing]
    def miniexp_substring(p: bytes, len: int) -> miniexp_t:
        """Construct a miniexp by copying at most n bytes of a string.

        The same as miniexp_lstring from the perspective of the Python FFI.

        Args:
            len: The number of bytes.
            p: The byte encoding of a string.

        Returns:
            A string miniexp.
        """


if not TYPE_CHECKING:
    miniexp_concat = libdjvulibre.cdll.miniexp_concat
    miniexp_concat.argtypes = [miniexp_t]
    miniexp_concat.restype = miniexp_t
else:
    def miniexp_concat(l: miniexp_t) -> miniexp_t:
        """Concatenate all direct string subexpressions in a list into a single string miniexp.

        Args:
            l: The list miniexp to concatenate.

        Returns:
            The concatenated string. If the argument is a cyclic list, return the empty list.
        """


# Lists
miniexp_nil = miniexp_t()
"""An empty miniexp list.

This is a Python implementation of the corresponding header-defined value.
"""


miniexp_dummy = miniexp_t.from_address(2)
"""An invalid miniexp used to represent various exceptional conditions.

This is a Python implementation of the corresponding header-defined value.
"""


def miniexp_listp(p: miniexp_t) -> bool:
    """Test if a miniexp is either a pair or an empty list.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a pair or empty list.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.LIST


def miniexp_consp(p: miniexp_t) -> bool:
    """Test if a miniexp is a pair.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is a pair.
    """
    return not p.is_null and miniexp_listp(p)


if not TYPE_CHECKING:
    miniexp_length = libdjvulibre.cdll.miniexp_length
    miniexp_length.argtypes = [miniexp_t]
    miniexp_length.restype = ctypes.c_int
else:
    def miniexp_length(p: miniexp_t) -> miniexp_t:
        """Get the length of a list miniexp.

        Args:
            p: Any miniexp.

        Returns:
            The length of `p` if it is a regular list miniexp; 0 for non-lists and -1 for circular lists.
        """


def miniexp_car(p: miniexp_t) -> miniexp_t:
    """Get the first component of a pair.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        The first component of `p` if it is a pair and the empty list otherwise.
    """
    if miniexp_consp(p):
        return miniexp_t.from_address(p.address)

    return miniexp_nil


def miniexp_cdr(p: miniexp_t) -> miniexp_t:
    """Get the second component of a pair.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        The first component of `p` if it is a pair and the empty list otherwise.
    """
    if miniexp_consp(p):
        return miniexp_t.from_address(p.address + ctypes.alignment(ctypes.c_void_p))

    return miniexp_nil


if not TYPE_CHECKING:
    miniexp_caar = libdjvulibre.cdll.miniexp_caar
    miniexp_caar.argtypes = [miniexp_t]
    miniexp_caar.restype = miniexp_t
else:
    def miniexp_caar(p: miniexp_t) -> miniexp_t:
        """Get the first component of the first component of a pair.

        Args:
            p: Any miniexp.

        Returns:
            The corresponding nested component of `p`, if it exists, and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_cdar = libdjvulibre.cdll.miniexp_cdar
    miniexp_cdar.argtypes = [miniexp_t]
    miniexp_cdar.restype = miniexp_t
else:
    def miniexp_cdar(p: miniexp_t) -> miniexp_t:
        """Get the second component of the first component of a pair.

        Args:
            p: Any miniexp.

        Returns:
            The corresponding nested component of `p`, if it exists, and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_cadr = libdjvulibre.cdll.miniexp_cadr
    miniexp_cadr.argtypes = [miniexp_t]
    miniexp_cadr.restype = miniexp_t
else:
    def miniexp_cadr(p: miniexp_t) -> miniexp_t:
        """Get the first component of the second component of a pair.

        Args:
            p: Any miniexp.

        Returns:
            The corresponding nested component of `p`, if it exists, and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_cddr = libdjvulibre.cdll.miniexp_cddr
    miniexp_cddr.argtypes = [miniexp_t]
    miniexp_cddr.restype = miniexp_t
else:
    def miniexp_cddr(p: miniexp_t) -> miniexp_t:
        """Get the second component of the second component of a pair.

        Args:
            p: Any miniexp.

        Returns:
            The corresponding nested component of `p`, if it exists, and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_caddr = libdjvulibre.cdll.miniexp_caddr
    miniexp_caddr.argtypes = [miniexp_t]
    miniexp_caddr.restype = miniexp_t
else:
    def miniexp_caddr(p: miniexp_t) -> miniexp_t:
        """Get the first component of the second component of the second component of a pair.

        Args:
            p: Any miniexp.

        Returns:
            The corresponding nested component of `p`, if it exists, and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_cdddr = libdjvulibre.cdll.miniexp_cdddr
    miniexp_cdddr.argtypes = [miniexp_t]
    miniexp_cdddr.restype = miniexp_t
else:
    def miniexp_cdddr(p: miniexp_t) -> miniexp_t:
        """Get the second component of second component of the second component of a pair.

        Args:
            p: Any miniexp.

        Returns:
            The corresponding nested component of `p`, if it exists, and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_nth = libdjvulibre.cdll.miniexp_nth
    miniexp_nth.argtypes = [ctypes.c_int, miniexp_t]
    miniexp_nth.restype = miniexp_t
else:
    def miniexp_nth(n: int, l: miniexp_t) -> miniexp_t:
        """Get the n-th element of a list.

        Args:
            n: A nonnegative index.
            l: Any miniexp.

        Returns:
            The corresponding element of `p`, if it exists, and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_cons = libdjvulibre.cdll.miniexp_cons
    miniexp_cons.__doc__ = 'Construct a pair miniexp.'
    miniexp_cons.argtypes = [miniexp_t, miniexp_t]
    miniexp_cons.restype = miniexp_t
else:
    def miniexp_cons(car: miniexp_t | None, cdr: miniexp_t | None) -> miniexp_t:
        """Construct a pair miniexp.

        Args:
            car: The nullable first component.
            cdr: The nullable second component.

        Returns:
            A pair miniexp.
        """


if not TYPE_CHECKING:
    miniexp_rplaca = libdjvulibre.cdll.miniexp_rplaca
    miniexp_rplaca.argtypes = [miniexp_t, miniexp_t]
    miniexp_rplaca.restype = miniexp_t
else:
    def miniexp_rplaca(pair: miniexp_t, newcar: miniexp_t) -> miniexp_t:
        """Replace the first component of a pair in-place.

        Args:
            pair: The pair to modify.
            newcar: The second component.

        Returns:
            The new first component if `pair` is a list and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_rplacd = libdjvulibre.cdll.miniexp_rplacd
    miniexp_rplacd.argtypes = [miniexp_t, miniexp_t]
    miniexp_rplacd.restype = miniexp_t
else:
    def miniexp_rplacd(pair: miniexp_t, newcdr: miniexp_t) -> miniexp_t:
        """Replace the second component of a pair in-place.

        Args:
            pair: The pair to modify.
            newcdr: The first component.

        Returns:
            The new first component if `pair` is a list and the empty list otherwise.
        """


if not TYPE_CHECKING:
    miniexp_reverse = libdjvulibre.cdll.miniexp_reverse
    miniexp_reverse.argtypes = [miniexp_t]
    miniexp_reverse.restype = miniexp_t
else:
    def miniexp_reverse(p: miniexp_t) -> miniexp_t:
        """Destructively reverse a list.

        Args:
            p: The throwaway list to reverse.

        Returns:
            The reverse of `p` if it is a list and the empty list otherwise.
        """
