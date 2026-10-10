"""A module for locating and loading libdjvulibre."""
# mypy: disable-error-code=empty-body

import ctypes
import importlib
import platform
import sys
from typing import TYPE_CHECKING

from .exceptions import DjvuLibreLibraryLoadError


def _load_libdjvulibre_impl(soname_version: int) ->  ctypes.CDLL:
    match sys.platform:
        case 'win32':
            # ruff: ignore[import-outside-top-level]
            from djvulibre_bin import get_latest_available_libdjvulibre_version, get_libdjvulibre_resource

            djvulibre_version = get_latest_available_libdjvulibre_version(soname_version)
            traversable = get_libdjvulibre_resource('windows', platform.machine(), djvulibre_version)

            with importlib.resources.as_file(traversable) as path:
                return ctypes.CDLL(str(path))
        case 'darwin':
            return ctypes.CDLL(f'libdjvulibre.{soname_version}.dylib')
        case _:
            return ctypes.CDLL(f'libdjvulibre.so.{soname_version}')


def load_libdjvulibre(soname_version: int) ->  ctypes.CDLL:
    """Load libdjvulibre for a given C API version.

    Args:
        soname_version: The C API ("soname") version.

    Returns:
        A ctypes wrapper around the library.

    Raises:
        OSError: If loading fails.
    """
    try:
        return _load_libdjvulibre_impl(soname_version)
    except OSError as err:
        raise DjvuLibreLibraryLoadError('Could not find a supported version of libdjvulibre') from err


libdjvulibre = load_libdjvulibre(soname_version=21)
"""A ctypes wrapper around libdjvulibre."""


if not TYPE_CHECKING:
    ddjvu_get_version_string = libdjvulibre.ddjvu_get_version_string
    ddjvu_get_version_string.argtypes = []
    ddjvu_get_version_string.restype = ctypes.c_char_p
else:
    def ddjvu_get_version_string() -> bytes:
        """Get a version string of the loaded library."""
