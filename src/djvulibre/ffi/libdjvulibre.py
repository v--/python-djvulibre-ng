"""A ctypes FFI for libdjvulibre.

This module takes care of property loading the library.
The modules ddjvuapi and miniexp imitate the corresponding headers that constitute the official public API.
"""

import ctypes
import os


if os.name == 'nt':  # TODO: Figure out dynamic linking on Windows
    libdjvulibre = ctypes.cdll.LoadLibrary('libdjvulibre')
else:
    libdjvulibre = ctypes.cdll.LoadLibrary('libdjvulibre.so.21')


ddjvu_get_version_string = libdjvulibre.ddjvu_get_version_string
ddjvu_get_version_string.__doc__ = 'Get a version string of the loaded library.'
ddjvu_get_version_string.argtypes = []
ddjvu_get_version_string.restype = ctypes.c_char_p
