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
    """Class for annotating overrides of automated ctypes annotations.

    Args:
        override: The type to use for ctypes's argument system.
    """

    override: type
    """The type to use for ctypes's argument system."""


def _map_type_hint(hint: type) -> type:
    if (metadata := getattr(hint, '__metadata__', None)):
        for item in metadata:
            if isinstance(item, CType):
                return item.override

    return hint


def wrap_dll_function_extended(dll: ctypes.CDLL) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Wrap a function from a dynamic library based on a Python function's type hint.

    Based on the Python 3.16 method with the same name, but with added support for return type overrides.

    Args:
        dll: The ctypes library wrapper.

    Returns:
        A decorator that takes a Python function and exposes the corresponding FFI function based on its name and type.
    """

    def decorator(fun: Callable[P, R]) -> Callable[P, R]:
        hints = typing.get_type_hints(fun, include_extras=True)
        impl = getattr(dll, fun.__name__)
        impl.restype = _map_type_hint(hints.pop('return'))
        impl.argtypes = [_map_type_hint(hint) for hint in hints.values()]
        functools.update_wrapper(impl, fun)
        return impl

    return decorator
