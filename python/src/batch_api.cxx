#include <pybind11/pybind11.h>
#include "box2d_wrapper.hpp"
#include "helper.hxx"

#include "apis/debug_draw_api.hxx"
#include "debug_draw/pyb2Draw.hxx"
#include "debug_draw/batch_debug_draw_caller.hxx"

#include <iostream>
#include <initializer_list>


namespace py = pybind11;


// functions without any argument 
// and b2Vec2 as output
#define VEC2_GETTER(PY_NAME, CPP_NAME)\
    .def(#PY_NAME, [](self_type & self, np_vec2_row_major & out){\
        with_vec2_array(out, [&](auto vec2_out, auto  n_sources){\
            for(std::size_t i=0; i<self.size(); ++i){\
                vec2_out[i] = self[i]->CPP_NAME();\
            }\
        });\
        return out;\
    }, py::arg("out"))


// functions without any argument returning scalar
#define SCALAR_GETTER(PY_NAME, CPP_NAME, T)\
    .def(#PY_NAME, [](self_type & self, cstyle_array<T>  & out){\
        auto out_1d = out.mutable_unchecked<1>();\
        for(std::size_t i=0; i<self.size(); ++i){\
            out_1d(i) = self[i]->CPP_NAME();\
        }\
        return out;\
    }, py::arg("out"))


template<class T>
class BatchVector : protected std::vector<T *>
{
public:
    using base_type = std::vector<T*>;
    using value_type = typename base_type::value_type;
    using base_type::size;
    using base_type::push_back;
    using base_type::begin;
    using base_type::end;
    using base_type::erase;
    using base_type::operator[];
private:
};


class JointVector : public BatchVector<b2Joint>
{
public:
};



class BodyVector : public BatchVector<b2Body>
{
public:
};


template<class CLS, class PY_CLS>
void add_batch_api(
    PY_CLS & py_cls, 
    const std::string & cls_name,
    const std::string & entity_name
)
{
    using self_type = CLS;
    // value type is b2Body* / b2Joint* / T *
    using ptr_type  = typename self_type::value_type;

    py_cls
        .def(py::init<>())

        // size
        .def("__len__", [](const self_type & self){
            return self.size();
        },"get the length")

        // append item
        .def("append", [](self_type & self, ptr_type item){
            self.push_back(item);
         },
            R"""(
                Add entry to the vector

                Warning:
                    When this function is called with a item already present in the vector
                    a duplicate will be added. No checks are performed to avoid this.

                Args:
                    item (Item): item to add
            )"""
        )

        // remove item if item is present
        .def("remove", [](self_type & self, ptr_type item){
            auto iter = std::find(self.begin(), self.end(), item);
            if(iter != self.end())
            {
                self.erase(iter);
            }
        },
            R"""(
                Remove item from Vector

                When this function is called with a item not present in Vector nothing happens.

                Args:
                    item (Item): item to remove
            )"""
        )
    ;
}


void exportBodyBatchApi(py::module & pybox2dModule){

    using self_type = BodyVector;
    auto py_cls =  py::class_<self_type>(pybox2dModule, "_BodyVector");
    add_batch_api<self_type>(py_cls, "Body", "body");

    py_cls

        // batch queries:
        .def("apply_force_to_center", [](
            self_type & self,
            np_vec2_row_major forces,
            bool wake
        ){
            with_vec2_array(forces, [&](auto vec2_forces, auto  n){
                for(std::size_t i=0; i<self.size(); ++i)
                {
                    self[i]->ApplyForceToCenter(
                        vec2_forces[std::max(std::size_t(1), n)],
                        wake
                    );
                }
            });
        },
            py::arg("force"),
            py::arg("wake") = true, 
            R"""(
                Apply a force to center of each body.

                If a [1x2] array is passed, the same force is applied to each body.

                Args:
                    force (numpy.ndarray[numpy.float32]): [n_bodies x 2] or [1 x 2] arrays
                        with the force vector for each body.
                    wake (bool): wake sleeping bodies 
            )"""
        )
        
        .def("apply_gravitonal_forces_to_center", [](
            self_type & self,
            np_vec2_row_major gravity_source_location,
            np_vec2_row_major gravity_source_strength,
            bool wake
        ){
            if(gravity_source_location.ndim() != 2 || gravity_source_strength.ndim() !=1)
            {
                throw std::runtime_error("input arrays have wrong dimensions");
            }
            if(gravity_source_location.shape(1) != 2 )
            {
                throw std::runtime_error("wrong shape: needs to be [X,2]");
            }
            if(gravity_source_location.shape(0) != gravity_source_strength.shape(0) and gravity_source_strength.shape(0) != 1)
            {
                throw std::runtime_error("gravity_source_location and gravity_source_strength shape mismatch");
            }

            const auto n_strength = gravity_source_strength.shape(0);
            auto uc_gravity_source_strength = gravity_source_strength.unchecked<1>();

            with_vec2_array(gravity_source_location, [&](auto vec2_locations, auto  n_sources){


                for(std::size_t source_index=0; source_index<n_sources; ++source_index)
                {
                    const auto & pos = vec2_locations[source_index];
                    const auto strength = (n_strength == 1) ? uc_gravity_source_strength(0) : uc_gravity_source_strength(source_index);

                    for(const auto & body : self)
                    {
                        auto delta = pos - body->GetPosition();
                        const auto d = delta.Normalize();
                        const auto force = delta * strength * body->GetMass() / (d*d);
                        body->ApplyForceToCenter(force, wake);
                    }
                }
            });
        },
            py::arg("position"),
            py::arg("strength"),
            py::arg("wake") = true,
            R"""(
                Apply gravitational forces from multiple sources.

                Apply gravitational forces, attractive and/or repulsive from multiple
                gravitational sources.

                The gravitational force between to bodies is given by:

                    F = G *  m1 * m2  / r**2

                Let `m1` be the mass of a body in the BodyVector and `m2` be
                the mass of the `gravitational source`. We can reinterpret/abuse
                `G * m2` as the `gravitational strength`. This quantity is passed
                to the functions with the argument `strength`.
                

                Args:
                    position (numpy.ndarray[numpy.float32]): [n x 2] array with locations
                        of gravity source

                    strength (numpy.ndarray[numpy.float32]): [n] array with scalar gravity strengths
                        for each gravity source. The strength the product between the the mass of the `gravity-source`
                        times the gravitational constant. A positive value leads to attractive force, a negative value
                        to repulsive forces.
            )"""
        )


        
        VEC2_GETTER(_position,         GetPosition)
        VEC2_GETTER(_world_center,     GetWorldCenter)
        VEC2_GETTER(_local_center,     GetLocalCenter)
        VEC2_GETTER(_linear_velocity,  GetLinearVelocity)
        // #undef VEC2_GETTER


        SCALAR_GETTER(_angle,              GetAngle,           float)
        SCALAR_GETTER(_angular_velocity,   GetAngularVelocity, float)
        SCALAR_GETTER(_mass,               GetMass,            float)
        SCALAR_GETTER(_inertia,            GetInertia,         float)       
        SCALAR_GETTER(_linear_damping,     GetLinearDamping,   float)     
        SCALAR_GETTER(_angular_damping,    GetAngularDamping,  float)    

        SCALAR_GETTER(_bullet,              IsBullet,           bool)     
        SCALAR_GETTER(_sleeping_allowed,    IsSleepingAllowed,  bool)     
        SCALAR_GETTER(_awake,               IsAwake,            bool)     
        SCALAR_GETTER(_enabled,             IsEnabled,          bool)     
        SCALAR_GETTER(_fixed_rotation,      IsFixedRotation,    bool)     
        // #undef SCALAR_GETTER

    ;
}



template<class CLS, class PY_CLS>
void add_joint_base_batch_api(
    PY_CLS & py_cls
)
{
    using self_type = CLS;
    using ptr_type  = typename self_type::value_type;

    py_cls
    ;
        //.def(py::init<>())

}



void exportJointBatchApi(py::module & pybox2dModule){

    {
        using self_type = BatchVector<b2Joint>;
        auto py_cls =  py::class_<self_type>(pybox2dModule, "_JointVector");
        add_batch_api<self_type>(py_cls, "Joint", "joint");
        add_joint_base_batch_api<self_type>(py_cls);

        py_cls
        ;
    }
    {
        using self_type = BatchVector<b2DistanceJoint>;
        auto py_cls =  py::class_<self_type>(pybox2dModule, "_DistanceJointVector");
        add_batch_api<self_type>(py_cls, "DistanceJoint", "joint");
        add_joint_base_batch_api<self_type>(py_cls);

        py_cls
        SCALAR_GETTER(_length, GetLength, float)
        ;
    }
}

void exportBatchApi(py::module & pybox2dModule){
    exportBodyBatchApi(pybox2dModule);
    exportJointBatchApi(pybox2dModule);
}