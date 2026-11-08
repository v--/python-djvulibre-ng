from . import list as list_miniexp
from . import number as number_miniexp
from . import object as object_miniexp
from . import string as string_miniexp
from . import symbol as symbol_miniexp


def test_miniexp_classof_number() -> None:
    expr = number_miniexp.miniexp_number(7)
    assert object_miniexp.miniexp_classof(expr) == list_miniexp.miniexp_nil


def test_miniexp_classof_string() -> None:
    expr = string_miniexp.miniexp_string(b'test')
    assert symbol_miniexp.miniexp_to_name(object_miniexp.miniexp_classof(expr)) == b'string'


def test_miniexp_isa_string_failure() -> None:
    expr = number_miniexp.miniexp_number(7)
    class_expr = symbol_miniexp.miniexp_symbol(b'string')
    assert object_miniexp.miniexp_isa(expr, class_expr) == list_miniexp.miniexp_nil


def test_miniexp_isa_string_success() -> None:
    expr = string_miniexp.miniexp_string(b'string')
    class_expr = symbol_miniexp.miniexp_symbol(b'string')
    assert symbol_miniexp.miniexp_to_name(object_miniexp.miniexp_isa(expr, class_expr)) == b'string'
