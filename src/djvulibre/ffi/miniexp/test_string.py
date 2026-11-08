import ctypes

from . import list as list_miniexp
from . import number as number_miniexp
from . import string as string_miniexp


class TestMiniexpStringCreation:
    def test_miniexp_string(self) -> None:
        expr = string_miniexp.miniexp_string(b'test')
        assert string_miniexp.miniexp_stringp(expr)
        assert string_miniexp.miniexp_to_str(expr) == b'test'

    def test_miniexp_lstring_length_in_bounds(self) -> None:
        expr = string_miniexp.miniexp_lstring(3, b'test')
        assert string_miniexp.miniexp_stringp(expr)
        assert string_miniexp.miniexp_to_str(expr) == b'tes'

    def test_miniexp_lstring_length_outside_bounds(self) -> None:
        expr = string_miniexp.miniexp_lstring(5, b'test')
        assert string_miniexp.miniexp_stringp(expr)
        assert string_miniexp.miniexp_to_str(expr) == b'test'

    def test_miniexp_substring_length_in_bounds(self) -> None:
        expr = string_miniexp.miniexp_substring(b'test', 3)
        assert string_miniexp.miniexp_stringp(expr)
        assert string_miniexp.miniexp_to_str(expr) == b'tes'

    def test_miniexp_substring_length_outside_bounds(self) -> None:
        expr = string_miniexp.miniexp_substring(b'test', 5)
        assert string_miniexp.miniexp_stringp(expr)
        assert string_miniexp.miniexp_to_str(expr) == b'test'


class TestMiniexpStringConcat:
    def test_miniexp_concat_empty_list(self) -> None:
        expr = string_miniexp.miniexp_concat(list_miniexp.miniexp_nil)
        assert string_miniexp.miniexp_stringp(expr)
        assert string_miniexp.miniexp_to_str(expr) == b''

    def test_miniexp_concat_cyclic_list(self) -> None:
        expr = list_miniexp.miniexp_cons(list_miniexp.miniexp_nil, list_miniexp.miniexp_nil)
        list_miniexp.miniexp_rplacd(expr, expr)
        assert string_miniexp.miniexp_concat(expr) == list_miniexp.miniexp_nil

    def test_miniexp_concat_two_element_list(self) -> None:
        a = string_miniexp.miniexp_string(b'a')
        b = string_miniexp.miniexp_string(b'b')
        lst = list_miniexp.miniexp_cons(a, list_miniexp.miniexp_cons(b, list_miniexp.miniexp_nil))
        combined = string_miniexp.miniexp_concat(lst)

        assert string_miniexp.miniexp_stringp(combined)
        assert string_miniexp.miniexp_to_str(combined) == b'ab'


class TestMiniexpStringMisc:
    def test_miniexp_to_lstr(self) -> None:
        expr = string_miniexp.miniexp_string(b'test')
        c_string = ctypes.c_char_p()
        assert string_miniexp.miniexp_to_lstr(expr, ctypes.pointer(c_string)) == 4
        assert c_string.value == b'test'

    def test_miniexp_to_lstr_invlid(self) -> None:
        expr = number_miniexp.miniexp_number(7)
        c_string = ctypes.c_char_p()
        assert string_miniexp.miniexp_to_lstr(expr, ctypes.pointer(c_string)) == 0
        assert c_string.value is None
