# python-djvulibre-ng

This project implements bindings for [`libdjvulibre`](https://djvu.sourceforge.net/). It is merely a prototype at the moment --- I want to stress-test some basics as much as possible prior to committing to it.

Goals:

* Bindings for `ddjvuapi.h` and `miniexp.h` (perhaps a higher-level API can be added later).
* [Free threading](https://docs.python.org/3/howto/free-threading-python.html) support.
* [Static typing](https://typing.python.org/en/latest/).
* A modern build system ([meson-python](https://pypi.org/project/meson-python/) with [pybind11](https://pypi.org/project/pybind11/)).
* Linux, Windows and macOS support.
* Tests with public domain books (generating test data for specific cases turns out to be more difficult).
* I plan to use `GPL-2.0-or-later`, like DjVuLibre itself, compared to `GPL-2.0-only` for [python-djvulibre](https://github.com/jwilk-archive/python-djvulibre) (the reason why I started this project from scratch instead of contributing).
