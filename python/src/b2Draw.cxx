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
        pyCls
            .def(py::init<const py::object &, const bool >())

            .def_property("flags",
                [](PyB2Draw * draw){return draw->GetFlags();},
                [](PyB2Draw * draw,const int flag){draw->SetFlags(flag);}
            )
            .def("reset_bounding_box",&PyB2Draw::resetBoundingBox)
            .def_property_readonly("bounding_box", &PyB2Draw::getBoundingBox)
            .def("_append_flags_int",[](PyB2Draw * draw,const int flag){draw->AppendFlags(flag);})
            .def("_clear_flags_int",[](PyB2Draw * draw,const int flag){draw->ClearFlags(flag);})

            .def_readwrite("screen_size",&PyB2Draw::m_screen_size)
            .def_readwrite("scale",&PyB2Draw::m_scale)
            .def_readwrite("translate",&PyB2Draw::m_translate)
            .def_readwrite("flip_y",&PyB2Draw::m_flip_y)
    
        ;
    }
    {
        auto pyCls = py::class_<BatchDebugDrawCaller>(pybox2dModule, "BatchDebugDrawCaller");
        add_debug_draw_api<BatchDebugDrawCaller>(pyCls);
        pyCls
            .def(py::init<const py::object &>())
            .def("_append_flags_int",[](BatchDebugDrawCaller * draw,const int flag){draw->AppendFlags(flag);})
            .def("_clear_flags_int",[](BatchDebugDrawCaller * draw,const int flag){draw->ClearFlags(flag);})

            .def_readwrite("screen_size",&BatchDebugDrawCaller::m_screen_size)
            .def_readwrite("scale",&BatchDebugDrawCaller::m_scale)
            .def_readwrite("translate",&BatchDebugDrawCaller::m_translate)
            .def_readwrite("flip_y",&BatchDebugDrawCaller::m_flip_y)
        ;
    }
}


