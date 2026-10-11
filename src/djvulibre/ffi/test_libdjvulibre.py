# This would fail if loading the dynamic library raises an exception
def test_libdjvulibre_loading() -> None:
    # ruff: ignore[import-outside-top-level]
    from . import libdjvulibre
    assert libdjvulibre.ddjvu_get_version_string().startswith(b'DjVuLibre')
