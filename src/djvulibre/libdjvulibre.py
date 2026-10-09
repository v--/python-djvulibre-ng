import ctypes
import os


if os.name == 'nt':  # TODO: Figure out dynamic linking on Windows
    libdjvulibre = ctypes.cdll.LoadLibrary('libdjvulibre')
else:
    libdjvulibre = ctypes.cdll.LoadLibrary('libdjvulibre.so.21')


libdjvulibre.ddjvu_get_version_string.argtypes = []
libdjvulibre.ddjvu_get_version_string.restype = ctypes.c_char_p
