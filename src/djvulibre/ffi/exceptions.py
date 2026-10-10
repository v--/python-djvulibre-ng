from djvulibre.exceptions import DjvuLibreError


class DjvuLibreFFIError(DjvuLibreError):
    pass


class DjvuLibreLibraryLoadError(DjvuLibreFFIError):
    pass
