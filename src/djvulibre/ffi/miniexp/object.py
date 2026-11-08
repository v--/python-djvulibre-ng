"""Functions for object S-expressions.

This is one of the four primary kinds of S-expressions.
"""
# mypy: disable-error-code=empty-body

from djvulibre.ffi.libdjvulibre import libdjvulibre
from djvulibre.ffi.miniexp.miniexp_t import MiniExpInternalKind

from .miniexp_t import miniexp_t


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
