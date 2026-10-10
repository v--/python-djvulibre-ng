import ctypes

import pytest

from . import miniexp


class TestMiniexpNumber:
    def xtest_miniexp_number(self) -> None:
        expr = miniexp.miniexp_number(7)
        assert miniexp.miniexp_numberp(expr)
        assert miniexp.miniexp_to_int(expr) == 7

    def xtest_miniexp_number_zero(self) -> None:
        # Ensure that no null pointer mess happens here.
        expr = miniexp.miniexp_number(0)
        assert miniexp.miniexp_numberp(expr)
        assert miniexp.miniexp_to_int(expr) == 0

    def xtest_miniexp_number_large(self) -> None:
        with pytest.raises(OverflowError):
            miniexp.miniexp_number(2 ** 64)


class TestMiniexpString:
    # String miniexp construction
    def test_miniexp_string(self) -> None:
        expr = miniexp.miniexp_string(b'test')
        assert miniexp.miniexp_stringp(expr)
        assert miniexp.miniexp_to_str(expr) == b'test'

    def test_miniexp_lstring_length_in_bounds(self) -> None:
        expr = miniexp.miniexp_lstring(3, b'test')
        assert miniexp.miniexp_stringp(expr)
        assert miniexp.miniexp_to_str(expr) == b'tes'

    def test_miniexp_lstring_length_outside_bounds(self) -> None:
        expr = miniexp.miniexp_lstring(5, b'test')
        assert miniexp.miniexp_stringp(expr)
        assert miniexp.miniexp_to_str(expr) == b'test'

    def test_miniexp_substring_length_in_bounds(self) -> None:
        expr = miniexp.miniexp_substring(b'test', 3)
        assert miniexp.miniexp_stringp(expr)
        assert miniexp.miniexp_to_str(expr) == b'tes'

    def test_miniexp_substring_length_outside_bounds(self) -> None:
        expr = miniexp.miniexp_substring(b'test', 5)
        assert miniexp.miniexp_stringp(expr)
        assert miniexp.miniexp_to_str(expr) == b'test'

    # Other string miniexp methods
    def test_miniexp_to_lstr(self) -> None:
        expr = miniexp.miniexp_string(b'test')
        c_string = ctypes.c_char_p()
        assert miniexp.miniexp_to_lstr(expr, ctypes.pointer(c_string)) == 4
        assert c_string.value == b'test'

    def xtest_miniexp_concat_empty_list(self) -> None:
        combined = miniexp.miniexp_concat(miniexp.miniexp_nil)
        assert miniexp.miniexp_to_str(combined) == b''

    def xtest_miniexp_concat_two_element_list(self) -> None:
        a = miniexp.miniexp_string(b'a')
        b = miniexp.miniexp_string(b'b')
        lst = miniexp.miniexp_cons(a, miniexp.miniexp_cons(b, miniexp.miniexp_nil))
        combined = miniexp.miniexp_concat(lst)

        assert miniexp.miniexp_to_str(combined) == b'ab'


class TestMiniexpList:
    class TestMiniexpListp:
        def xtest_miniexp_listp_empty(self) -> None:
            assert miniexp.miniexp_listp(miniexp.miniexp_nil)

        def test_miniexp_listp_string(self) -> None:
            expr = miniexp.miniexp_string(b'test')
            assert not miniexp.miniexp_listp(expr)

        def test_miniexp_listp_cons(self) -> None:
            expr = miniexp.miniexp_cons(None, None)
            assert miniexp.miniexp_listp(expr)

    class TestMiniexpConsp:
        def xtest_miniexp_consp_empty(self) -> None:
            assert not miniexp.miniexp_consp(miniexp.miniexp_nil)

        def test_miniexp_consp_cons(self) -> None:
            expr = miniexp.miniexp_cons(None, None)
            assert miniexp.miniexp_listp(expr)

    class TestMiniexpLength:
        def test_miniexp_length_invalid(self) -> None:
            # As per the documentation, the length of non-lists is 0
            expr = miniexp.miniexp_string(b'test')
            assert miniexp.miniexp_length(expr) == 0

        def test_miniexp_length_empty(self) -> None:
            assert miniexp.miniexp_length(miniexp.miniexp_nil) == 0

        def xtest_miniexp_length_cons(self) -> None:
            value = miniexp.miniexp_number(1)
            expr = miniexp.miniexp_cons(value, miniexp.miniexp_nil)
            assert miniexp.miniexp_length(expr) == 1

        def xtest_miniexp_length_cons2(self) -> None:
            value = miniexp.miniexp_number(1)
            expr = miniexp.miniexp_cons(value, miniexp.miniexp_cons(value, miniexp.miniexp_nil))
            assert miniexp.miniexp_length(expr) == 2
