"""Bindings for the custom S-expressions ("miniexp") from DjVuLibre.

A recreation of the miniexp.h API of libdjvulibre using a ctypes FFI.
"""

from .floatnum import miniexp_doublep, miniexp_floatnum, miniexp_floatnump, miniexp_to_double
from .list import (
    miniexp_caar,
    miniexp_caddr,
    miniexp_cadr,
    miniexp_car,
    miniexp_cdar,
    miniexp_cdddr,
    miniexp_cddr,
    miniexp_cdr,
    miniexp_cons,
    miniexp_consp,
    miniexp_dummy,
    miniexp_length,
    miniexp_listp,
    miniexp_nil,
    miniexp_nth,
    miniexp_reverse,
    miniexp_rplaca,
    miniexp_rplacd,
)
from .miniexp_t import miniexp_t
from .number import miniexp_number, miniexp_numberp, miniexp_to_int
from .object import (
    miniexp_classof,
    miniexp_isa,
    miniexp_objectp,
)
from .string import (
    miniexp_concat,
    miniexp_lstring,
    miniexp_string,
    miniexp_stringp,
    miniexp_substring,
    miniexp_to_lstr,
    miniexp_to_str,
)
from .symbol import miniexp_symbol, miniexp_symbolp, miniexp_to_name
