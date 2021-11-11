#include <pybind11/pybind11.h>

#include <box2d/box2d.h>


namespace py = pybind11;

#include "holder.hxx"
#include "user_data.hxx"

class PyB2Joint : public b2Joint {
public:
    using b2Joint::b2Joint;
    virtual ~PyB2Joint() {}

    /// Get the anchor point on bodyA in world coordinates.
    virtual b2Vec2 GetAnchorA() const {
        PYBIND11_OVERLOAD_PURE(
            b2Vec2,       // Return type 
            b2Joint,      // Parent class 
            GetAnchorA    // Name of function 
        );
        return b2Vec2();
    }

    /// Get the anchor point on bodyB in world coordinates.
    virtual b2Vec2 GetAnchorB() const {
        PYBIND11_OVERLOAD_PURE(
            b2Vec2,       // Return type 
            b2Joint,      // Parent class 
            GetAnchorB    // Name of function 
        );
        return b2Vec2();
    }

    /// Get the reaction force on bodyB at the joint anchor in Newtons.
    virtual b2Vec2 GetReactionForce(float inv_dt) const {
        PYBIND11_OVERLOAD_PURE(
            b2Vec2,       // Return type 
            b2Joint,      // Parent class 
            GetReactionForce,    // Name of function 
            inv_dt
        )
        return b2Vec2();
    }

    /// Get the reaction torque on bodyB in N*m.
    virtual float GetReactionTorque(float inv_dt) const {
        PYBIND11_OVERLOAD_PURE(
            float,       // Return type 
            b2Joint,      // Parent class 
            GetReactionTorque,    // Name of function 
            inv_dt
        );
        return float();
    }

    // They are protected
    virtual void InitVelocityConstraints(const b2SolverData& data){
        PYBIND11_OVERLOAD_PURE(
            void,       // Return type 
            b2Joint,      // Parent class 
            InitVelocityConstraints,    // Name of function 
            data
        );
    }
    virtual void SolveVelocityConstraints(const b2SolverData& data){
        PYBIND11_OVERLOAD_PURE(
            void,       // Return type 
            b2Joint,      // Parent class 
            SolveVelocityConstraints,    // Name of function 
            data
        );
    }
    virtual bool SolvePositionConstraints(const b2SolverData& data){
        PYBIND11_OVERLOAD_PURE(
            bool,       // Return type 
            b2Joint,      // Parent class 
            SolvePositionConstraints,    // Name of function 
            data
        );
        return false;
    }
};


template<class DT>
bool isType(const b2Joint * shape){
    return bool(dynamic_cast<const DT *>(shape));
}

template<class DT>
DT * asType(b2Joint * shape){
    auto res =  dynamic_cast<DT *>(shape);
    if(res == nullptr){
        throw std::runtime_error("invalid b2Joint dynamic cast");
    }
    return res;
}

class PyB2JointDef : public b2JointDef{
public:
    using b2JointDef::b2JointDef;
};

void exportb2Joint(py::module & pybox2dModule){

    pybox2dModule.def("linear_stiffness", [](float frequency_hertz, float damping_ratio, b2Body* bodyA, b2Body* bodyB){
        float stiffness;
        float damping;
        b2LinearStiffness(stiffness, damping, frequency_hertz, damping_ratio, bodyA, bodyB);
        return std::make_tuple(stiffness, damping);
    },
        py::arg("frequency_hz"),
        py::arg("damping_ratio"),
        py::arg("body_a"),
        py::arg("body_b")
    );
    pybox2dModule.def("angular_stiffness", [](float frequency_hertz, float damping_ratio, b2Body* bodyA, b2Body* bodyB){
        float stiffness;
        float damping;
        b2AngularStiffness(stiffness, damping, frequency_hertz, damping_ratio, bodyA, bodyB);
        return std::make_tuple(stiffness, damping);
    },
        py::arg("frequency_hz"),
        py::arg("damping_ratio"),
        py::arg("body_a"),
        py::arg("body_b")
    );

    py::enum_<b2JointType>(pybox2dModule, "JointType")
        .value("unknown_joint", b2JointType::e_unknownJoint)
        .value("revolute_joint", b2JointType::e_revoluteJoint)
        .value("prismatic_joint", b2JointType::e_prismaticJoint)
        .value("distance_joint", b2JointType::e_distanceJoint)
        .value("pulley_joint", b2JointType::e_pulleyJoint)
        .value("mouse_joint", b2JointType::e_mouseJoint)
        .value("gear_joint", b2JointType::e_gearJoint)
        .value("wheel_joint", b2JointType::e_wheelJoint)
        .value("weld_joint", b2JointType::e_weldJoint)
        .value("friction_joint", b2JointType::e_frictionJoint)
        //.value("rope_joint", b2JointType::e_ropeJoint)
        .value("motor_joint", b2JointType::e_motorJoint)
    ;

    // py::enum_<b2LimitState>(pybox2dModule, "b2LimitState")
    //     .value("inactive_limit", b2LimitState::e_inactiveLimit)
    //     .value("at_lower_limit", b2LimitState::e_atLowerLimit)
    //     .value("at_upper_limit", b2LimitState::e_atUpperLimit)
    //     .value("equal_limits", b2LimitState::e_equalLimits)
    // ;



    py::class_<b2JointEdge>(pybox2dModule, "JointEdge")
        // A lot to do
    ;

    auto jointCls = py::class_<b2Joint,JointHolder,  PyB2Joint>(pybox2dModule,"Joint");

    add_user_data_api<b2Joint>(jointCls);
    jointCls
        //.alias<b2Joint>()
       // .def(py::init<const b2JointDef* >())
        //
        .def_property_readonly("type",&b2Joint::GetType) 
        .def_property_readonly("body_a", [](b2Joint * self){
            return self->GetBodyA();
        })
        .def_property_readonly("body_b", [](b2Joint * self){
            return self->GetBodyB();
        })  
        .def_property_readonly("anchor_a",&b2Joint::GetAnchorA)
        .def_property_readonly("anchor_b",&b2Joint::GetAnchorB)     
        .def("get_reaction_force",&b2Joint::GetReactionForce, py::arg("iv_dt"))
        .def("get_reaction_torque",&b2Joint::GetReactionTorque, py::arg("iv_dt"))
        .def("_has_next", [](b2Joint * j){ return j->GetNext()!=nullptr;})
        .def("_get_next", [](b2Joint * j){return j->GetNext();}, py::return_value_policy::reference_internal)


        .def("_has_user_data",[](b2Joint * j){return j->GetUserData().pointer != 0;})
        .def("_set_user_data",[](b2Joint * j, const py::object & ud){
            auto ptr = new py::object(ud);
            j->GetUserData().pointer = reinterpret_cast<uintptr_t>(ptr);

        })
        .def("_get_user_data",[](b2Joint * j){
            auto vuserData = reinterpret_cast<void*>(j->GetUserData().pointer);
            auto ud = static_cast<py::object *>(vuserData);
            auto ret = py::object(*ud);
            return ret;
        })
        .def("_delete_user_data",[](b2Joint * j){
             auto vuserData = reinterpret_cast<void*>(j->GetUserData().pointer);
            auto ud = static_cast<py::object *>(vuserData);
            delete ud;
            j->GetUserData().pointer = 0;
        })

            // .def_dynamic_cast<b2Joint,b2DistanceJoint>("asDistanceJoint")
            // .def_dynamic_cast<b2Joint,b2FrictionJoint>("asFrictionJoint")
            // .def_dynamic_cast<b2Joint,b2GearJoint>("asGearJoint")
            // .def_dynamic_cast<b2Joint,b2PrismaticJoint>("asPrismaticJoint")
            // .def_dynamic_cast<b2Joint,b2PulleyJoint>("asPulleyJoint")
            // .def_dynamic_cast<b2Joint,b2RevoluteJoint>("asRevoluteJoint")
            // .def_dynamic_cast<b2Joint,b2RopeJoint>("asRopeJoint")
            // .def_dynamic_cast<b2Joint,b2WeldJoint>("asWeldJoint")
            // .def_dynamic_cast<b2Joint,b2WheelJoint>("asWheelJoint")
            // .def_dynamic_cast<b2Joint,b2MouseJoint>("asMouseJoint")

    ;
   
   
    py::class_<b2DistanceJoint,DistanceJointHolder, b2Joint>(pybox2dModule,"DistanceJoint")
        .def_property("length",&b2DistanceJoint::GetLength, &b2DistanceJoint::SetLength)
        .def_property("stiffness",&b2DistanceJoint::GetStiffness, &b2DistanceJoint::SetStiffness)
        .def_property("damping",&b2DistanceJoint::GetDamping, &b2DistanceJoint::SetDamping)
    ;  
    py::class_<b2FrictionJoint,Holder<b2FrictionJoint>, b2Joint>(pybox2dModule,"FrictionJoint");
    ;
    py::class_<b2GearJoint
        , Holder<b2GearJoint>, b2Joint 
    >(pybox2dModule,"GearJoint")
    ;
    py::class_<b2PrismaticJoint
        , Holder<b2PrismaticJoint>, b2Joint 
    >(pybox2dModule,"PrismaticJoint")
    ;
    py::class_<b2PulleyJoint
        , Holder<b2PulleyJoint>, b2Joint 
    >(pybox2dModule,"PulleyJoint")
    ;
    py::class_<b2RevoluteJoint
        , Holder<b2RevoluteJoint>, b2Joint 
    >(pybox2dModule,"RevoluteJoint")
    ;
    // py::class_<b2RopeJoint
    //     , Holder<b2RopeJoint>, b2Joint 
    // >(pybox2dModule,"RopeJoint")
    ;
    py::class_<b2WeldJoint
        , Holder<b2WeldJoint>, b2Joint 
    >(pybox2dModule,"WeldJoint")
    ;
    py::class_<b2WheelJoint
        , Holder<b2WheelJoint>, b2Joint 
    >(pybox2dModule,"WheelJoint")
        .def_property_readonly("joint_translation", &b2WheelJoint::GetJointTranslation)
        .def_property("motor_speed",&b2WheelJoint::GetMotorSpeed, &b2WheelJoint::SetMotorSpeed)
        .def_property("enable_motor",&b2WheelJoint::IsMotorEnabled, &b2WheelJoint::EnableMotor)
        .def_property("max_motor_torque",&b2WheelJoint::GetMaxMotorTorque, &b2WheelJoint::SetMaxMotorTorque)
        .def_property("damping",&b2WheelJoint::GetDamping, &b2WheelJoint::SetDamping)
        // .def_property("damping",&b2WheelJoint::GetSpringDampingRatio, &b2WheelJoint::SetSpringDampingRatio)
    ;
    py::class_<b2MouseJoint
        , Holder<b2MouseJoint>, b2Joint 
    >(pybox2dModule,"MouseJoint")
        .def_property("max_force",&b2MouseJoint::GetMaxForce, &b2MouseJoint::SetMaxForce)
        .def_property("target", &b2MouseJoint::GetTarget, &b2MouseJoint::SetTarget)
    ;
   

}

