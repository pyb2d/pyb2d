#include "pybind11/pybind11.h"

// #include "xtensor/xmath.hpp"
// #include "xtensor/xarray.hpp"

// #define FORCE_IMPORT_ARRAY
// #include "xtensor-python/pyarray.hpp"
// #include "xtensor-python/pyvectorize.hpp"

#include <iostream>
#include <numeric>
#include <string>
#include <sstream>

namespace py = pybind11;


namespace py = pybind11;
namespace pyb2d{
    void def_build_config(py::module &m);
}
void exportContact(py::module & );
void exportB2World(py::module & );
void exportB2Body(py::module & );
void exportB2Math(py::module & );
void exportB2Fixture(py::module & );
void exportB2Shape(py::module & );
void exportb2Joint(py::module & );
void exportb2JointDef(py::module & );
void exportB2WorldCallbacks(py::module & );
void exportB2Draw(py::module & );
void exportb2Collision(py::module & );
void exportBatchApi(py::module & );
#ifdef PYB2D_LIQUID_FUN
void exportB2Particle(py::module & );
void exportB2ParticleSystem(py::module & );
void exportB2ParticleGroup(py::module & );
void exportEmitter(py::module &);
#endif



// Python Module and Docstrings
PYBIND11_MODULE(_b2d , pyb2dModule)
{
    //xt::import_numpy();

    pyb2dModule.doc() = R"pbdoc(
        _pyb2d  python bindings

        .. currentmodule:: _pyb2d

        .. autosummary::
           :toctree: _generate

           BuildConfiguration
           MyClass
    )pbdoc";

    pyb2d::def_build_config(pyb2dModule);
    exportContact(pyb2dModule);
    exportB2World(pyb2dModule);
    exportB2Body(pyb2dModule);
    exportB2Math(pyb2dModule);
    exportB2Shape(pyb2dModule);
    exportB2Fixture(pyb2dModule);
    exportb2Joint(pyb2dModule);
    exportb2JointDef(pyb2dModule);
    exportB2WorldCallbacks(pyb2dModule);
    exportB2Draw(pyb2dModule);
    exportb2Collision(pyb2dModule);
    exportBatchApi(pyb2dModule);
    #ifdef PYB2D_LIQUID_FUN
    exportB2Particle(pyb2dModule);
    exportB2ParticleSystem(pyb2dModule);
    exportB2ParticleGroup(pyb2dModule);
    exportEmitter(pyb2dModule);
    #endif

    pyb2dModule.attr("__version__") = "0.7.5";
}
