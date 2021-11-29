#include <pybind11/pybind11.h>
#include "box2d_wrapper.hpp"


#include "apis/debug_draw_api.hxx"
#include "debug_draw/pyb2Draw.hxx"
#include "debug_draw/batch_debug_draw_caller.hxx"

#include <iostream>
#include <initializer_list>


namespace py = pybind11;



void exportB2Draw(py::module & pybox2dModule){


    py::class_<b2Color>(pybox2dModule, "Color")
        .def(py::init([](py::tuple t) { 
            if(py::len(t) != 3)
            {
                throw std::runtime_error("tuple has wrong length");
            }
            return new b2Color(
                    t[0].cast<float>(), 
                    t[1].cast<float>(),
                    t[2].cast<float>()
                ); 
            }
        )) 


        .def_readwrite("r",&b2Color::r)
        .def_readwrite("g",&b2Color::g)
        .def_readwrite("b",&b2Color::b)
    ;
    py::implicitly_convertible<py::tuple, b2Color>();

    {
        auto pyCls = py::class_<PyB2Draw>(pybox2dModule,"DrawCaller");
        add_debug_draw_api<PyB2Draw>(pyCls);
        add_debug_draw_transform_api<PyB2Draw>(pyCls);
        pyCls
            .def(py::init<const py::object &, const bool >())

            .def_property("flags",
                [](PyB2Draw * draw){return draw->GetFlags();},
                [](PyB2Draw * draw,const int flag){draw->SetFlags(flag);}
            )
            .def("reset_bounding_box",&PyB2Draw::resetBoundingBox)
            .def_property_readonly("bounding_box", &PyB2Draw::getBoundingBox)
    
        ;
    }
    {
        using batch_debug_draw_type = BatchDebugDrawCaller<uint8_t, float, true>;
        auto pyCls = py::class_<batch_debug_draw_type >(pybox2dModule, "BatchDebugDrawCaller_uint8_float_True");
        add_debug_draw_api<batch_debug_draw_type>(pyCls);
        add_debug_draw_transform_api<batch_debug_draw_type>(pyCls);
        pyCls
            .def(py::init<const py::object &>())

        ;
    }

    // for kivy backend (float colors, float coordinates, no transform)
    {
        using batch_debug_draw_type = BatchDebugDrawCaller<float, float, false>;
        auto pyCls = py::class_<batch_debug_draw_type >(pybox2dModule, "BatchDebugDrawCaller_float_float_False");
        add_debug_draw_api<batch_debug_draw_type>(pyCls);
        pyCls
            .def(py::init<const py::object &>())
          
        ;
    }
    // for ipycanvas and pygame backend (uint8 colors, int32 coordinates, with transform)
    {
        using batch_debug_draw_type = BatchDebugDrawCaller<uint8_t, int32_t, true>;
        auto pyCls = py::class_<batch_debug_draw_type >(pybox2dModule, "BatchDebugDrawCaller_uint8_int32_True");
        add_debug_draw_api<batch_debug_draw_type>(pyCls);
        add_debug_draw_transform_api<batch_debug_draw_type>(pyCls);
        pyCls
            .def(py::init<const py::object &>())
          
        ;
    }
}


