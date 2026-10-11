"""A module for locating and loading libdjvulibre."""
# mypy: disable-error-code=empty-body

import ctypes
import importlib
import platform
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .exceptions import DjVuLibreLibraryLoadError


# We try to determine the API version based on the changelog of symbol changes between API versions in miniexp.h
def _determine_api_version(cdll: ctypes.CDLL, soname_version: int) -> int:
    if soname_version != 21:
        raise DjVuLibreLibraryLoadError(f'Cannot detect the API version for soname version {soname_version}')

    if getattr(cdll, 'miniexp_to_lstr', None):
        # Note that DDJVUAPI_VERSION in DjVuLibre v3.5.30.1 is set to 23 even though the heading states that miniexp_to_lstr is added in 24.
        return 24

    raise DjVuLibreLibraryLoadError('API versions below 24 are not supported')


@dataclass
class LibDjVuLibre:
    """A ctypes wrapper around libdjvulibre with versions attached.

    Args:
        cdll: The ctypes wrapper.
        soname_version: The loaded soname version.
        api_version: The loaded C API version.
            If not specified, so we try to determine it based on the symbol available.

    Raises:
        DjVuLibreLibraryLoadError: If detecting the API version fails.
    """

    cdll: ctypes.CDLL
    """The ctypes wrapper."""

    soname_version: int
    """The loaded soname version."""

    api_version: int
    """The loaded C API version.

    Note that the DDJVUAPI_VERSION constant in ddjvuapi.h mistakenly reports the API version as 23 instead of 24.
    """

    def __init__(self, cdll: ctypes.CDLL, soname_version: int, api_version: int | None = None) -> None:
        self.cdll = cdll
        self.soname_version = soname_version

        if api_version is None:
            self.api_version = _determine_api_version(cdll, soname_version)
        else:
            self.api_version = api_version


def _load_libdjvulibre_cdll(soname_version: int) ->  ctypes.CDLL:
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


def load_libdjvulibre(soname_versions: Sequence[int]) -> LibDjVuLibre:
    """Load libdjvulibre for a list of available soname version.

    Args:
        soname_versions: The list of soname versions.

    Returns:
        A ctypes wrapper around the library with version information.

    Raises:
        DjVuLibreLibraryLoadError: If loading all given versions fails.
    """
    for soname_version in soname_versions:
        try:
            cdll = _load_libdjvulibre_cdll(soname_version)
            return LibDjVuLibre(cdll, soname_version)
        except OSError:
            pass
        else:
            continue

    raise DjVuLibreLibraryLoadError('Could not find supported version of libdjvulibre')


libdjvulibre = load_libdjvulibre(soname_versions=[21])
"""A ctypes wrapper around libdjvulibre."""


if not TYPE_CHECKING:
    ddjvu_get_version_string = libdjvulibre.cdll.ddjvu_get_version_string
    ddjvu_get_version_string.argtypes = []
    ddjvu_get_version_string.restype = ctypes.c_char_p
else:
    def ddjvu_get_version_string() -> bytes:
        """Get a version string of the loaded library."""
