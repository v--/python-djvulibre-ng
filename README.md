# python-djvulibre-ng

[![Tests](https://github.com/v--/python-djvulibre-ng/actions/workflows/test.yml/badge.svg)](https://github.com/v--/python-djvulibre-ng/actions/workflows/test.yml)

This project implements bindings for [`libdjvulibre`](https://djvu.sourceforge.net/). It is merely a prototype at the moment --- I want to stress-test some of the basics as much as possible prior to committing to it. I am currently stuck at making compilation on Windows work reliably.

Goals:

* [ctypes](https://docs.python.org/3/library/ctypes.html)-based bindings for `ddjvuapi.h` and `miniexp.h` (perhaps a higher-level API can be added later).
* [Free threading](https://docs.python.org/3/howto/free-threading-python.html) support.
* [Static typing](https://typing.python.org/en/latest/).
* Linux, Windows and macOS support.
* Tests with public domain books (generating test data for specific cases turns out to be more difficult).
* I plan to use `GPL-2.0-or-later`, like DjVuLibre itself, compared to `GPL-2.0-only` for [python-djvulibre](https://github.com/jwilk-archive/python-djvulibre) (the reason why I started this project from scratch instead of contributing).

## Prerequisites

On UNIX systems, we rely on `djvulibre` being installed and discoverable. On Windows, due to the lack of [RPATH](https://en.wikipedia.org/wiki/Rpath) support (see the `meson-python` docs [here](https://mesonbuild.com/meson-python/how-to-guides/shared-libraries.html)), we include `djvulibre` itself as a submodule (for extracting header files) and [`djvulibre-bin`](https://github.com/v--/djvulibre-bin) with precompiled Windows libraries get embedded in the wheel file.
