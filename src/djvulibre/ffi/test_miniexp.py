import ctypes

import pytest

from djvulibre.ffi.libdjvulibre import libdjvulibre

from . import miniexp


class TestMiniexpNumber:
    def test_miniexp_number(self) -> None:
        expr = miniexp.miniexp_number(7)
        assert miniexp.miniexp_numberp(expr)
        assert miniexp.miniexp_to_int(expr) == 7

    def test_miniexp_number_zero(self) -> None:
        # Ensure that no null pointer mess happens here.
        expr = miniexp.miniexp_number(0)
        assert miniexp.miniexp_numberp(expr)
        assert miniexp.miniexp_to_int(expr) == 0

    def test_miniexp_number_large(self) -> None:
        with pytest.raises(OverflowError):
            miniexp.miniexp_number(2 ** 64)


class TestMiniexpString:
    class TestMiniexpStringCreation:
        def test_miniexp_string(self) -> None:
            expr = miniexp.miniexp_string(b'test')
            assert miniexp.miniexp_stringp(expr)
            assert miniexp.miniexp_to_str(expr) == b'test'

        @pytest.mark.skipif(libdjvulibre.api_version < 24, reason='`miniexp_lstring` is not available')
        def test_miniexp_lstring_length_in_bounds(self) -> None:
            expr = miniexp.miniexp_lstring(3, b'test')
            assert miniexp.miniexp_stringp(expr)
            assert miniexp.miniexp_to_str(expr) == b'tes'

        @pytest.mark.skipif(libdjvulibre.api_version < 24, reason='`miniexp_lstring` is not available')
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

    class TestMiniexpStringConcat:
        def test_miniexp_concat_empty_list(self) -> None:
            expr = miniexp.miniexp_concat(miniexp.miniexp_nil)
            assert miniexp.miniexp_stringp(expr)
            assert miniexp.miniexp_to_str(expr) == b''

        def test_miniexp_concat_cyclic_list(self) -> None:
            expr = miniexp.miniexp_cons(miniexp.miniexp_nil, miniexp.miniexp_nil)
            miniexp.miniexp_rplacd(expr, expr)
            assert miniexp.miniexp_concat(expr) == miniexp.miniexp_nil

        def test_miniexp_concat_two_element_list(self) -> None:
            a = miniexp.miniexp_string(b'a')
            b = miniexp.miniexp_string(b'b')
            lst = miniexp.miniexp_cons(a, miniexp.miniexp_cons(b, miniexp.miniexp_nil))
            combined = miniexp.miniexp_concat(lst)

            assert miniexp.miniexp_stringp(combined)
            assert miniexp.miniexp_to_str(combined) == b'ab'

    class TestMiniexpStringMisc:
        @pytest.mark.skipif(libdjvulibre.api_version < 24, reason='`miniexp_to_lstr` is not available')
        def test_miniexp_to_lstr(self) -> None:
            expr = miniexp.miniexp_string(b'test')
            c_string = ctypes.c_char_p()
            assert miniexp.miniexp_to_lstr(expr, ctypes.pointer(c_string)) == 4
            assert c_string.value == b'test'

        @pytest.mark.skipif(libdjvulibre.api_version < 24, reason='`miniexp_to_lstr` is not available')
        def test_miniexp_to_lstr_invlid(self) -> None:
            expr = miniexp.miniexp_number(7)
            c_string = ctypes.c_char_p()
            assert miniexp.miniexp_to_lstr(expr, ctypes.pointer(c_string)) == 0
            assert c_string.value is None


class TestMiniexpList:
    class TestMiniexpListp:
        def test_miniexp_listp_empty(self) -> None:
            assert miniexp.miniexp_listp(miniexp.miniexp_nil)

        def test_miniexp_listp_string(self) -> None:
            expr = miniexp.miniexp_string(b'test')
            assert not miniexp.miniexp_listp(expr)

        def test_miniexp_listp_cons(self) -> None:
            expr = miniexp.miniexp_cons(None, None)
            assert miniexp.miniexp_listp(expr)

    class TestMiniexpConsp:
        def test_miniexp_consp_empty(self) -> None:
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

        def test_miniexp_length_cons(self) -> None:
            value = miniexp.miniexp_number(1)
            expr = miniexp.miniexp_cons(value, miniexp.miniexp_nil)
            assert miniexp.miniexp_length(expr) == 1

        def test_miniexp_length_cons2(self) -> None:
            value = miniexp.miniexp_number(1)
            expr = miniexp.miniexp_cons(value, miniexp.miniexp_cons(value, miniexp.miniexp_nil))
            assert miniexp.miniexp_length(expr) == 2

        def test_miniexp_length_cyclic(self) -> None:
            expr = miniexp.miniexp_cons(miniexp.miniexp_nil, miniexp.miniexp_nil)
            miniexp.miniexp_rplacd(expr, expr)
            assert miniexp.miniexp_length(expr) == -1

    class TestMiniexpAccess:
        def test_miniexp_car_cdr(self) -> None:
            car = miniexp.miniexp_number(1)
            cdr = miniexp.miniexp_number(2)
            expr = miniexp.miniexp_cons(car, cdr)
            assert miniexp.miniexp_car(expr) == car
            assert miniexp.miniexp_cdr(expr) == cdr

        def test_miniexp_caar_to_cddr(self) -> None:
            caar = miniexp.miniexp_number(1)
            cadr = miniexp.miniexp_number(2)
            cdar = miniexp.miniexp_number(3)
            cddr = miniexp.miniexp_number(4)

            expr = miniexp.miniexp_cons(
                miniexp.miniexp_cons(caar, cdar),
                miniexp.miniexp_cons(cadr, cddr),
            )

            assert miniexp.miniexp_caar(expr) == caar
            assert miniexp.miniexp_cadr(expr) == cadr
            assert miniexp.miniexp_cdar(expr) == cdar
            assert miniexp.miniexp_cddr(expr) == cddr

        def test_miniexp_nth(self) -> None:
            a = miniexp.miniexp_number(1)
            b = miniexp.miniexp_number(2)
            c = miniexp.miniexp_number(3)

            expr = miniexp.miniexp_cons(a,
                miniexp.miniexp_cons(b,
                    miniexp.miniexp_cons(c, miniexp.miniexp_nil),
                ),
            )

            assert miniexp.miniexp_length(expr) == 3
            assert miniexp.miniexp_nth(0, expr) == a
            assert miniexp.miniexp_nth(1, expr) == b
            assert miniexp.miniexp_nth(2, expr) == c

    class TestMiniexpMutation:
        def test_miniexp_rplaca_valid(self) -> None:
            car = miniexp.miniexp_number(1)
            cdr = miniexp.miniexp_number(2)
            expr = miniexp.miniexp_cons(car, cdr)

            return_value = miniexp.miniexp_rplaca(expr, cdr)

            assert miniexp.miniexp_car(expr) == cdr
            assert return_value == cdr

        def test_miniexp_rplaca_invalid(self) -> None:
            expr = miniexp.miniexp_number(7)
            replacement = miniexp.miniexp_number(3)

            return_value = miniexp.miniexp_rplaca(expr, replacement)
            assert return_value == miniexp.miniexp_nil

        def test_miniexp_rplacd(self) -> None:
            car = miniexp.miniexp_number(1)
            cdr = miniexp.miniexp_number(2)
            expr = miniexp.miniexp_cons(car, cdr)

            return_value = miniexp.miniexp_rplacd(expr, car)

            assert miniexp.miniexp_car(expr) == car
            assert return_value == car

        def test_miniexp_reverse(self) -> None:
            a = miniexp.miniexp_number(1)
            b = miniexp.miniexp_number(2)
            c = miniexp.miniexp_number(3)

            expr = miniexp.miniexp_cons(a,
                miniexp.miniexp_cons(b,
                    miniexp.miniexp_cons(c, miniexp.miniexp_nil),
                ),
            )

            reversed_ = miniexp.miniexp_reverse(expr)

            assert miniexp.miniexp_length(reversed_) == 3
            assert miniexp.miniexp_nth(0, reversed_) == c
            assert miniexp.miniexp_nth(1, reversed_) == b
            assert miniexp.miniexp_nth(2, reversed_) == a
