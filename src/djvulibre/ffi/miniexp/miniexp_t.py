"""The core miniexp data type."""
# ruff: file-ignore[invalid-class-name]
# mypy: disable-error-code=empty-body

import ctypes
from enum import IntEnum
from typing import Self


class miniexp_t(ctypes.c_void_p):
    """An opaque pointer to a miniexp."""

    @property
    def address(self) -> int:
        return self.value or 0

    @property
    def is_null(self) -> bool:
        return self.value is None

    def __hash__(self) -> int:
        return self.address

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ctypes.c_void_p):
            return self.address == (other.value or 0)

        if isinstance(other, int):
            return self.address == other

        return False


class MiniExpInternalKind(IntEnum):
    """Python-only enum with internal DjVuLibre codes of miniexp expressions."""
    LIST = 0
    OBJECT = 1
    SYMBOL = 2
    NUMBER = 3

    @classmethod
    def from_miniexp(cls, p: miniexp_t) -> Self:
        return cls(p.address & 3)
