"""A ctypes FFI for libdjvulibre.

This module takes care of property loading the library.
The modules ddjvuapi and miniexp imitate the corresponding headers that constitute the official public API.
"""
import ctypes
import importlib
import os
import platform


if os.name == 'nt':
    from djvulibre_bin import get_libdjvulibre_resource

    traversable = get_libdjvulibre_resource('windows', platform.machine(), '3.5.30.1')

    with importlib.resources.as_file(traversable) as path:
        libdjvulibre = ctypes.CDLL(str(path))
else:
    libdjvulibre = ctypes.cdll.LoadLibrary('libdjvulibre.so.21')


ddjvu_get_version_string = libdjvulibre.ddjvu_get_version_string
ddjvu_get_version_string.__doc__ = 'Get a version string of the loaded library.'
ddjvu_get_version_string.argtypes = []
ddjvu_get_version_string.restype = ctypes.c_char_p
