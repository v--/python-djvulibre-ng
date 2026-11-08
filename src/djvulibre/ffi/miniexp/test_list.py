from . import list as list_miniexp
from . import number as number_miniexp
from . import string as string_miniexp


class TestMiniexpListp:
    def test_miniexp_listp_empty(self) -> None:
        assert list_miniexp.miniexp_listp(list_miniexp.miniexp_nil)

    def test_miniexp_listp_string(self) -> None:
        expr = string_miniexp.miniexp_string(b'test')
        assert not list_miniexp.miniexp_listp(expr)

    def test_miniexp_listp_cons(self) -> None:
        expr = list_miniexp.miniexp_cons(None, None)
        assert list_miniexp.miniexp_listp(expr)


class TestMiniexpConsp:
    def test_miniexp_consp_empty(self) -> None:
        assert not list_miniexp.miniexp_consp(list_miniexp.miniexp_nil)

    def test_miniexp_consp_cons(self) -> None:
        expr = list_miniexp.miniexp_cons(None, None)
        assert list_miniexp.miniexp_listp(expr)


class TestMiniexpLength:
    def test_miniexp_length_invalid(self) -> None:
        # As per the documentation, the length of non-lists is 0
        expr = string_miniexp.miniexp_string(b'test')
        assert list_miniexp.miniexp_length(expr) == 0

    def test_miniexp_length_empty(self) -> None:
        assert list_miniexp.miniexp_length(list_miniexp.miniexp_nil) == 0

    def test_miniexp_length_cons(self) -> None:
        value = number_miniexp.miniexp_number(1)
        expr = list_miniexp.miniexp_cons(value, list_miniexp.miniexp_nil)
        assert list_miniexp.miniexp_length(expr) == 1

    def test_miniexp_length_cons2(self) -> None:
        value = number_miniexp.miniexp_number(1)
        expr = list_miniexp.miniexp_cons(value, list_miniexp.miniexp_cons(value, list_miniexp.miniexp_nil))
        assert list_miniexp.miniexp_length(expr) == 2

    def test_miniexp_length_cyclic(self) -> None:
        expr = list_miniexp.miniexp_cons(list_miniexp.miniexp_nil, list_miniexp.miniexp_nil)
        list_miniexp.miniexp_rplacd(expr, expr)
        assert list_miniexp.miniexp_length(expr) == -1


class TestMiniexpAccess:
    def test_miniexp_car_cdr(self) -> None:
        car = number_miniexp.miniexp_number(1)
        cdr = number_miniexp.miniexp_number(2)
        expr = list_miniexp.miniexp_cons(car, cdr)
        assert list_miniexp.miniexp_car(expr) == car
        assert list_miniexp.miniexp_cdr(expr) == cdr

    def test_miniexp_caar_to_cddr(self) -> None:
        caar = number_miniexp.miniexp_number(1)
        cadr = number_miniexp.miniexp_number(2)
        cdar = number_miniexp.miniexp_number(3)
        cddr = number_miniexp.miniexp_number(4)

        expr = list_miniexp.miniexp_cons(
            list_miniexp.miniexp_cons(caar, cdar),
            list_miniexp.miniexp_cons(cadr, cddr),
        )

        assert list_miniexp.miniexp_caar(expr) == caar
        assert list_miniexp.miniexp_cadr(expr) == cadr
        assert list_miniexp.miniexp_cdar(expr) == cdar
        assert list_miniexp.miniexp_cddr(expr) == cddr

    def test_miniexp_nth(self) -> None:
        a = number_miniexp.miniexp_number(1)
        b = number_miniexp.miniexp_number(2)
        c = number_miniexp.miniexp_number(3)

        expr = list_miniexp.miniexp_cons(a,
            list_miniexp.miniexp_cons(b,
                list_miniexp.miniexp_cons(c, list_miniexp.miniexp_nil),
            ),
        )

        assert list_miniexp.miniexp_length(expr) == 3
        assert list_miniexp.miniexp_nth(0, expr) == a
        assert list_miniexp.miniexp_nth(1, expr) == b
        assert list_miniexp.miniexp_nth(2, expr) == c


class TestMiniexpMutation:
    def test_miniexp_rplaca_valid(self) -> None:
        car = number_miniexp.miniexp_number(1)
        cdr = number_miniexp.miniexp_number(2)
        expr = list_miniexp.miniexp_cons(car, cdr)

        return_value = list_miniexp.miniexp_rplaca(expr, cdr)

        assert list_miniexp.miniexp_car(expr) == cdr
        assert return_value == cdr

    def test_miniexp_rplaca_invalid(self) -> None:
        expr = number_miniexp.miniexp_number(7)
        replacement = number_miniexp.miniexp_number(3)

        return_value = list_miniexp.miniexp_rplaca(expr, replacement)
        assert return_value == list_miniexp.miniexp_nil

    def test_miniexp_rplacd(self) -> None:
        car = number_miniexp.miniexp_number(1)
        cdr = number_miniexp.miniexp_number(2)
        expr = list_miniexp.miniexp_cons(car, cdr)

        return_value = list_miniexp.miniexp_rplacd(expr, car)

        assert list_miniexp.miniexp_car(expr) == car
        assert return_value == car

    def test_miniexp_reverse(self) -> None:
        a = number_miniexp.miniexp_number(1)
        b = number_miniexp.miniexp_number(2)
        c = number_miniexp.miniexp_number(3)

        expr = list_miniexp.miniexp_cons(a,
            list_miniexp.miniexp_cons(b,
                list_miniexp.miniexp_cons(c, list_miniexp.miniexp_nil),
            ),
        )

        reversed_ = list_miniexp.miniexp_reverse(expr)

        assert list_miniexp.miniexp_length(reversed_) == 3
        assert list_miniexp.miniexp_nth(0, reversed_) == c
        assert list_miniexp.miniexp_nth(1, reversed_) == b
        assert list_miniexp.miniexp_nth(2, reversed_) == a
