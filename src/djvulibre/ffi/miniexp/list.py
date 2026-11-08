"""Functions for list S-expressions.

This is one of the four primary kinds of S-expressions.
"""
# mypy: disable-error-code=empty-body

import ctypes
from typing import Annotated

from djvulibre.ffi.ctypes_helpers import CType
from djvulibre.ffi.libdjvulibre import libdjvulibre
from djvulibre.ffi.miniexp.miniexp_t import MiniExpInternalKind

from .miniexp_t import miniexp_t


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
