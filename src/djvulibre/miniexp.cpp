#include <pybind11/pybind11.h>
#include <libdjvu/miniexp.h>

namespace py = pybind11;

PYBIND11_MODULE(miniexp, m, py::mod_gil_not_used()) {
    m.doc() = "Library for handling lisp expressions.";
    py::class_<minivar_t>(m, "minivar_t", "Opaque pointer type representing a lisp expression.");
}
