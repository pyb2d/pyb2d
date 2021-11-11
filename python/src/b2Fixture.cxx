#include <pybind11/pybind11.h>

#include <box2d/box2d.h>


#include "holder.hxx"


namespace py = pybind11;


    inline void setShape(b2FixtureDef & f, b2Shape * s){
                f.shape = s;
    }


    inline void fooFunc(const b2Shape * s){
        //std::cout<<"FOOO\n";
    }

void exportB2Fixture(py::module & pybox2dModule){


    pybox2dModule.def("fooFunc",&fooFunc);

    py::class_<b2Filter>(pybox2dModule,"Filter")
        .def(py::init<>())
        .def_readwrite("category_bits", &b2Filter::categoryBits)
        .def_readwrite("mask_bits", &b2Filter::maskBits)
        .def_readwrite("group_index", &b2Filter::groupIndex)
    ;




    py::class_<b2FixtureDef>(pybox2dModule,"FixtureDef")
        .def(py::init<>())
        .def("_set_shape",  //[](b2FixtureDef & f, b2Shape * s){f.shape = s;}, 
                &setShape,
            py::keep_alive<1,2>()
        )
        .def_readonly("_shape", &b2FixtureDef::shape)
        //.def_readwrite("userData", &b2FixtureDef::userData)
        .def_readwrite("friction", &b2FixtureDef::friction)
        .def_readwrite("restitution", &b2FixtureDef::restitution)
        .def_readwrite("density", &b2FixtureDef::density)
        .def_readwrite("is_sensor", &b2FixtureDef::isSensor)
        .def_readwrite("filter", &b2FixtureDef::filter)
        .def("_set_user_data",[](b2FixtureDef & b, const py::object & ud){
            auto ptr = new py::object(ud);
            b.userData.pointer = reinterpret_cast<uintptr_t>(ptr);
        })
        .def("_get_user_data",[](const b2FixtureDef & b){
            auto vuserData = reinterpret_cast<void*>(b.userData.pointer);
            auto ud = static_cast<py::object *>(vuserData);
            auto ret = py::object(*ud);
            return ret;
        })
        .def("_delete_userData",[](b2FixtureDef & b){
            auto vuserData = reinterpret_cast<void*>(b.userData.pointer);
            auto ud = static_cast<py::object *>(vuserData);
            delete ud;
            b.userData.pointer = 0;
        })
    ;

    py::class_<b2Fixture, FixtureHolder>(pybox2dModule,"Fixture")
        .def_property_readonly("type", &b2Fixture::GetType)
        .def("_getShape", [](b2Fixture & f) {return ShapeHolder(f.GetShape());})
        .def("set_Sensor", &b2Fixture::SetSensor,py::arg("sensor`"))
        .def_property_readonly("isSensor", &b2Fixture::IsSensor)

        .def_property_readonly("body", [](b2Fixture & f) {return f.GetBody();},
            py::return_value_policy::reference_internal
        )


        .def("_hasNext", [](b2Fixture &f){
            auto next = f.GetNext();
            return next != nullptr;
        })
        .def("_getNext", [](b2Fixture &f){
            auto next = f.GetNext();
            return next;
        }, py::return_value_policy::reference_internal)

        .def("_has_user_data",[](b2Fixture & b){return b.GetUserData().pointer!=0;})
        .def("_set_user_data",[](b2Fixture & b, const py::object & ud){
            auto ptr = new py::object(ud);
            b.GetUserData().pointer = reinterpret_cast<uintptr_t>(ptr);
        })
        .def("_get_user_data",[](b2Fixture & b){
            auto vuserData = reinterpret_cast<void*>(b.GetUserData().pointer);
            auto ud = static_cast<py::object *>(vuserData);
            auto ret = py::object(*ud);
            return ret;
        })
        .def("_delete_U_serData",[](b2Fixture & b){
            auto vuserData = reinterpret_cast<void*>(b.GetUserData().pointer);
            auto ud = static_cast<py::object *>(vuserData);
            delete ud;
            b.GetUserData().pointer  = 0;
        })
        .def("test_point",&b2Fixture::TestPoint)

        .def_property_readonly("type",&b2Fixture::GetType)
    ;

}

