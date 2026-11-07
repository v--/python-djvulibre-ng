"""Bindings for the custom S-expressions ("miniexp") from DjVuLibre.

An recreation of the miniexp.h API of libdjvulibre using a ctypes FFI.
"""
# ruff: file-ignore[invalid-class-name]
# mypy: disable-error-code=empty-body

import ctypes
import sys
from enum import IntEnum
from typing import Annotated, Self

from .ctypes_helpers import CType
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


@libdjvulibre.wrap_function
def miniexp_length(p: miniexp_t) -> Annotated[int, CType(ctypes.c_int)]:
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


@libdjvulibre.wrap_function
def miniexp_caar(p: miniexp_t) -> miniexp_t:
    """Get the first component of the first component of a pair.

    Args:
        p: Any miniexp.

    Returns:
        The corresponding nested component of `p`, if it exists, and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_cdar(p: miniexp_t) -> miniexp_t:
    """Get the second component of the first component of a pair.

    Args:
        p: Any miniexp.

    Returns:
        The corresponding nested component of `p`, if it exists, and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_cadr(p: miniexp_t) -> miniexp_t:
    """Get the first component of the second component of a pair.

    Args:
        p: Any miniexp.

    Returns:
        The corresponding nested component of `p`, if it exists, and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_cddr(p: miniexp_t) -> miniexp_t:
    """Get the second component of the second component of a pair.

    Args:
        p: Any miniexp.

    Returns:
        The corresponding nested component of `p`, if it exists, and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_caddr(p: miniexp_t) -> miniexp_t:
    """Get the first component of the second component of the second component of a pair.

    Args:
        p: Any miniexp.

    Returns:
        The corresponding nested component of `p`, if it exists, and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_cdddr(p: miniexp_t) -> miniexp_t:
    """Get the second component of second component of the second component of a pair.

    Args:
        p: Any miniexp.

    Returns:
        The corresponding nested component of `p`, if it exists, and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_nth(n: Annotated[int, CType(ctypes.c_int)], l: miniexp_t) -> miniexp_t:
    """Get the n-th element of a list.

    Args:
        n: A nonnegative index.
        l: Any miniexp.

    Returns:
        The corresponding element of `p`, if it exists, and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_cons(
    car: Annotated[miniexp_t | None, CType(miniexp_t)],
    cdr: Annotated[miniexp_t | None, CType(miniexp_t)],
) -> miniexp_t:
    """Construct a pair miniexp.

    Args:
        car: The nullable first component.
        cdr: The nullable second component.

    Returns:
        A pair miniexp.
    """


@libdjvulibre.wrap_function
def miniexp_rplaca(pair: miniexp_t, newcar: miniexp_t) -> miniexp_t:
    """Replace the first component of a pair in-place.

    Args:
        pair: The pair to modify.
        newcar: The second component.

    Returns:
        The new first component if `pair` is a list and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_rplacd(pair: miniexp_t, newcdr: miniexp_t) -> miniexp_t:
    """Replace the second component of a pair in-place.

    Args:
        pair: The pair to modify.
        newcdr: The first component.

    Returns:
        The new first component if `pair` is a list and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_reverse(p: miniexp_t) -> miniexp_t:
    """Destructively reverse a list.

    Args:
        p: The throwaway list to reverse.

    Returns:
        The reverse of `p` if it is a list and the empty list otherwise.
    """


def miniexp_objectp(p: miniexp_t) -> bool:
    """Test if a miniexp is an object.

    This is a Python implementation of the corresponding header-defined function.

    Args:
        p: Any miniexp.

    Returns:
        Whether `p` is an object.
    """
    return MiniExpInternalKind.from_miniexp(p) == MiniExpInternalKind.OBJECT


@libdjvulibre.wrap_function
def miniexp_classof(p: miniexp_t) -> miniexp_t:
    """Get the symbolic class of a miniexp.

    Args:
        p: Any miniexp.

    Returns:
        A symbol miniexp with the class of `p` if it is an object and the empty list otherwise.
    """


@libdjvulibre.wrap_function
def miniexp_isa(p: miniexp_t, c: miniexp_t) -> miniexp_t:
    """Determine whether an object miniexp is an instance of (a subclass of) a class.

    Args:
        p: Any miniexp.
        c: A symbol miniexp with a class name.

    Returns:
        A symbol miniexp with the actual class name of `p` if it is an instance of `c` and the empty list otherwise.
    """


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


# Floats
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
