# This would fail if loading the dynamic library raises an exception
def test_libdjvulibre_loading() -> None:
    # ruff: ignore[import-outside-top-level]
    from . import libdjvulibre
    version = libdjvulibre.ddjvu_get_version_string()
    assert version is not None
    assert version.startswith(b'DjVuLibre')
