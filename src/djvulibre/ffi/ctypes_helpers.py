"""This module contains utilities for ctypes."""

import ctypes
import functools
import typing
from collections.abc import Callable
from dataclasses import dataclass
from typing import ParamSpec, TypeVar


P = ParamSpec('P')
R = TypeVar('R')


@dataclass
class CType:
    """Class for annotating overrides of automated ctypes annotations."""
    override: type


def _map_type_hint(hint: type) -> type:
    if (metadata := getattr(hint, '__metadata__', None)):
        for item in metadata:
            if isinstance(item, CType):
                return item.override

    match hint:
        case _ if hint is bytes or hint == bytes | None:
            return ctypes.c_char_p

        case _:
            return hint


def wrap_dll_function_extended(dll: ctypes.CDLL) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Wrap a function from a dynamic library based on a Python function's type hint.

    Based on the Python 3.16 method with the same name, but with added support for return type overrides.
    """

    def decorator(fun: Callable[P, R]) -> Callable[P, R]:
        hints = typing.get_type_hints(fun, include_extras=True)
        impl = getattr(dll, fun.__name__)
        impl.restype = _map_type_hint(hints.pop('return'))
        impl.argtypes = [_map_type_hint(hint) for hint in hints.values()]
        functools.update_wrapper(impl, fun)
        return impl

    return decorator
