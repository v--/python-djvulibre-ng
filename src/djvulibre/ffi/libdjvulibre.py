"""A module for locating and loading libdjvulibre."""
# mypy: disable-error-code=empty-body

import ctypes
import importlib
import logging
import os.path
import platform
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .exceptions import DjVuLibreLibraryLoadError


logger = logging.getLogger(__name__)


@dataclass
class LibDjVuLibre:
    """A ctypes wrapper around libdjvulibre with the soversion and API version attached.

    Args:
        cdll: The ctypes wrapper.
        soversion: The soversion supposedly loaded.
    """

    cdll: ctypes.CDLL
    """The ctypes wrapper."""

    supposed_soversion: int
    """The soversion supposedly loaded.

    Realistically, this should be 21.
    """

    estimated_api_version: int
    """The C API version determined by inspecting the loaded symbols.

    Realistically, this should be 24.

    Note that the DDJVUAPI_VERSION constant in ddjvuapi.h may mistakenly report the API version as 23 instead of 24.
    """

    def __init__(self, cdll: ctypes.CDLL, supposed_soversion: int) -> None:
        self.cdll = cdll
        self.supposed_soversion = supposed_soversion

        if supposed_soversion != 21:
            raise DjVuLibreLibraryLoadError(f'We provide no bindings for libdjvulibre with soversion {supposed_soversion}')

        if not getattr(cdll, 'miniexp_to_lstr', None):
            logger.warning(f'No symbol `miniexp_to_lstr` found in dynamic library at {cdll.name}.')
            # Note that DDJVUAPI_VERSION in DjVuLibre v3.5.30.1 is set to 23 even though the heading states that miniexp_to_lstr is added in 24.
            raise DjVuLibreLibraryLoadError(f'Cannot determine API version for {cdll.name}')

        self.estimated_api_version = 24


def _load_libdjvulibre_cdll(soversion: int) -> ctypes.CDLL:
    match sys.platform:
        case 'win32':
            # ruff: ignore[import-outside-top-level]
            from djvulibre_bin import get_latest_available_djvulibre_version, get_libdjvulibre_resource

            djvulibre_version = get_latest_available_djvulibre_version(soversion)
            traversable = get_libdjvulibre_resource('windows', platform.machine(), djvulibre_version)

            with importlib.resources.as_file(traversable) as path:
                return ctypes.CDLL(str(path))

        case 'darwin':
            lib_name = f'libdjvulibre.{soversion}.dylib'

            # Homebrew may require some magic
            #   See https://github.com/astral-sh/uv/issues/7764#issuecomment-3217899208
            try:
                return ctypes.CDLL(lib_name)
            except OSError:
                logger.warning(f'libdjvulibre with soversion {soversion} not found in standard darwin locations; searching the homebrew lib directory.')
                homebrew_prefix = os.getenv('HOMEBREW_PREFIX')

                if not homebrew_prefix:
                    raise

            return ctypes.CDLL(os.path.join(homebrew_prefix, 'lib', lib_name))

        case _:
            return ctypes.CDLL(f'libdjvulibre.so.{soversion}')


def load_libdjvulibre(soversions: Sequence[int]) -> LibDjVuLibre:
    """Load libdjvulibre for a list of available soversion.

    Args:
        soversions: The list of soversions.

    Returns:
        A ctypes wrapper around the library with version information.

    Raises:
        DjVuLibreLibraryLoadError: If loading all given versions fails.
    """
    cdll: ctypes.CDLL | None = None

    for soversion in soversions:
        env_name = f'LIBDJVULIBRE{soversion}'

        if env_path := os.getenv(env_name):
            logger.debug(f'Trying to load libdjvulibre from {env_name}={env_path!r}.')

            try:
                cdll = ctypes.CDLL(env_path)
            except OSError as err:
                raise DjVuLibreLibraryLoadError(f'Could not load libdjvulibre from variable {env_name}') from err

        try:
            cdll = _load_libdjvulibre_cdll(soversion)
        except OSError:
            logger.warning(f'Could not load libdjvulibre with soversion {soversion}.')
        else:
            break

    if cdll:
        return LibDjVuLibre(cdll, soversion)

    raise DjVuLibreLibraryLoadError('Could not find a supported version of libdjvulibre')


libdjvulibre = load_libdjvulibre(soversions=[21])
"""A ctypes wrapper around libdjvulibre."""


if not TYPE_CHECKING:
    ddjvu_get_version_string = libdjvulibre.cdll.ddjvu_get_version_string
    ddjvu_get_version_string.argtypes = []
    ddjvu_get_version_string.restype = ctypes.c_char_p
else:
    def ddjvu_get_version_string() -> bytes:
        """Get a version string of the loaded library."""
