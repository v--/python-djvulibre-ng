"""A module for locating and loading libdjvulibre."""
# mypy: disable-error-code=empty-body

import importlib
import logging
import os.path
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Annotated, ParamSpec, TypeVar

from .ctypes_helpers import CType, wrap_dll_function_extended
from .exceptions import DjVuLibreCtypesError, DjVuLibreLibraryLoadError


try:
    import ctypes
except ImportError as err:
    raise DjVuLibreCtypesError('Could not load the ctypes module') from err


logger = logging.getLogger(__name__)


P = ParamSpec('P')
R = TypeVar('R')


@dataclass
class LibDjVuLibre:
    """A ctypes wrapper around libdjvulibre with the soversion and API version attached.

    Args:
        cdll: The ctypes wrapper.
        supposed_soversion: The soversion supposedly loaded.
    """

    cdll: ctypes.CDLL
    """The ctypes wrapper."""

    supposed_soversion: int
    """The soversion supposedly loaded.

    Realistically, this should equal 21.
    """

    estimated_api_version: int
    """The C API version determined by inspecting the loaded symbols.

    Realistically, this should equal 24.

    Note that the DDJVUAPI_VERSION constant in ddjvuapi.h may mistakenly report the API version as 23 instead of 24.
    """

    def __init__(self, cdll: ctypes.CDLL, supposed_soversion: int) -> None:
        self.cdll = cdll
        self.supposed_soversion = supposed_soversion

        if supposed_soversion != 21:
            raise DjVuLibreLibraryLoadError(f'We provide no bindings for libdjvulibre with soversion {supposed_soversion}')

        if not getattr(cdll, 'miniexp_to_lstr', None):
            logger.warning(f"No symbol 'miniexp_to_lstr' found in dynamic library at {cdll._name}.")
            # Note that DDJVUAPI_VERSION in DjVuLibre v3.5.30.1 is set to 23 even though the heading states that miniexp_to_lstr is added in 24.
            raise DjVuLibreLibraryLoadError(f'Cannot determine API version for {cdll._name}')

        self.estimated_api_version = 24

    def wrap_function(self, fun: Callable[P, R]) -> Callable[P, R]:
        """Convenience wrapper for [`wrap_dll_function_extended`](...wrap_dll_function_extended).

        [`ViatException`](..ViatException).

        Args:
            fun: A function with no body whose type hints are used to call the wrapped FFI function.

        Returns:
            The wrapped FFI function.
        """
        return wrap_dll_function_extended(self.cdll)(fun)


def _load_libdjvulibre_cdll(soversion: int) -> ctypes.CDLL:
    match sys.platform:
        case 'win32':
            try:
                with importlib.resources.as_file(importlib.resources.files('djvulibre') / 'bin' / 'libdjvulibre') as path:
                    return ctypes.CDLL(str(path))
            except OSError as err:
                raise DjVuLibreLibraryLoadError('Could not load libdjvulibre.dll that is supposed to be embedded into the package.') from err

        case 'darwin':
            lib_name = f'libdjvulibre.{soversion}.dylib'

            # Homebrew may require some magic
            #   See https://github.com/astral-sh/uv/issues/7764#issuecomment-3217899208
            try:
                return ctypes.CDLL(lib_name)
            except OSError:
                logger.debug(f'An exception occurred while loading libdjvulibre with soversion {soversion} from standard darwin locations.', exc_info=True)
                logger.warning(f'Could not load libdjvulibre with soversion {soversion} from standard darwin locations. Searching the homebrew lib directory.')
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
            try:
                cdll = ctypes.CDLL(env_path)
            except OSError as err:
                logger.debug(f'An exception occurred while loading libdjvulibre from {env_name}={env_path!r}.', exc_info=True)
                raise DjVuLibreLibraryLoadError(f'Could not load libdjvulibre from path set by {env_name}') from err
        else:
            try:
                cdll = _load_libdjvulibre_cdll(soversion)
            except OSError:
                logger.debug(f'An exception occurred while loading libdjvulibre with soversion {soversion}.', exc_info=True)
                logger.warning(f'Could not load libdjvulibre with soversion {soversion}.')
            else:
                break

    if cdll:
        return LibDjVuLibre(cdll, soversion)

    raise DjVuLibreLibraryLoadError('Could not load a supported version of libdjvulibre')


libdjvulibre = load_libdjvulibre(soversions=[21])
"""A ctypes wrapper around libdjvulibre."""


@libdjvulibre.wrap_function
def ddjvu_get_version_string() -> Annotated[bytes | None, CType(ctypes.c_char_p)]:
    """Get a version string of the loaded library."""
