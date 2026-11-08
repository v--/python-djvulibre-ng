from . import symbol as symbol_miniexp


def test_miniexp_to_name() -> None:
    expr = symbol_miniexp.miniexp_symbol(b'test')
    assert symbol_miniexp.miniexp_symbolp(expr)
    assert symbol_miniexp.miniexp_to_name(expr) == b'test'
