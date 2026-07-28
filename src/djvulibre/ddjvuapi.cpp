#include <pybind11/pybind11.h>
#include <libdjvu/ddjvuapi.h>

namespace py = pybind11;

PYBIND11_MODULE(ddjvuapi, m, py::mod_gil_not_used()) {
    m.doc() = "DjVu Reference Library";
    m.attr("DDJVUAPI_VERSION") = DDJVUAPI_VERSION;
}
