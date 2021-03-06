#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include <iostream>
#include <numeric>

namespace py = pybind11;



namespace pyb2d {

    void def_build_config(py::module & m)
    {

        struct BuildConfiguration        {

        };


        py::class_<BuildConfiguration>(m, "BuildConfiguration",
        "This class show the compile/build configuration\n"
        "Of pyb2d\n"
        )
        .def_property_readonly_static("BOX_2D_VERSION", [](py::object /* self */) {
            #ifdef  PYB2D_LIQUID_FUN
            return "2.4.1";
            #else
            return "2.4.1";
            #endif
        })
        .def_property_readonly_static("DEBUG", [](py::object /* self */) {
            #ifdef  NDEBUG
            return false;
            #else
            return true;
            #endif
        })
        .def_property_readonly_static("LIQUID_FUN", [](py::object /* self */) {
            #ifdef  PYB2D_LIQUID_FUN
            return true;
            #else
            return false;
            #endif
        })
        .def_property_readonly_static("OLD_BOX2D", [](py::object /* self */) {
            #ifdef  PYB2D_OLD_BOX2D
            return true;
            #else
            return false;
            #endif
        })

;



    }

}
