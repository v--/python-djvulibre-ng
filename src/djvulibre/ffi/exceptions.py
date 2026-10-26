from djvulibre.exceptions import DjVuLibreError


class DjVuLibreFFIError(DjVuLibreError):
    pass


class DjVuLibreCtypesError(DjVuLibreFFIError, ImportError):
    pass


class DjVuLibreLibraryLoadError(DjVuLibreFFIError):
    pass
