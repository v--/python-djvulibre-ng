from djvulibre.exceptions import DjVuLibreError


class DjVuLibreFFIError(DjVuLibreError):
    pass


class DjVuLibreLibraryLoadError(DjVuLibreFFIError):
    pass
