from .libdjvulibre import libdjvulibre


def test_ddjvu_get_version_string() -> None:
    assert libdjvulibre.ddjvu_get_version_string().startswith(b'DjVuLibre')
