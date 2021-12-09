

#include <pybind11/pybind11.h>

#include "box2d_wrapper.hpp"
#include "extensions/b2Emitter.h"
#include "holder.hxx"

namespace py = pybind11;

void exportEmitter(py::module &pybox2dModule) {

    // BASE
    py::class_<b2EmitterDefBase> emitterDefBaseCls(pybox2dModule, "EmitterDefBase");
    emitterDefBaseCls.def(py::init<>())
        .def_readwrite("transform", &b2EmitterDefBase::transform)
        .def_property(
        "body",
        [](const b2EmitterDefBase *self) { return BodyHolder(self->body); },
        [](b2EmitterDefBase *self, b2Body *body) { self->body = body; })
        .def_readwrite("emite_rate", &b2EmitterDefBase::emitRate)
        .def_readwrite("lifetime", &b2EmitterDefBase::lifetime)
        .def_readwrite("enabled", &b2EmitterDefBase::enabled)
    ;

    py::class_<b2EmitterBase> emitterBaseCls(pybox2dModule, "EmitterBase");
    emitterBaseCls.def(py::init<b2ParticleSystem *, const b2EmitterDefBase &>())
    .def_property("position", &b2EmitterBase::GetPosition, &b2EmitterBase::SetPosition)
    .def_property("angle", &b2EmitterBase::GetAngle, &b2EmitterBase::SetAngle)
    .def_property("transform", &b2EmitterBase::GetTransform, &b2EmitterBase::SetTransform)
    .def_property("enabled", &b2EmitterBase::GetEnabled, &b2EmitterBase::SetEnabled)
    ;


    //  LINEAR Array
    py::class_<b2LinearEmitterArrayDef> linearEmitterArrayDefCls(pybox2dModule, "LinearEmitterArrayDef", emitterDefBaseCls);
    linearEmitterArrayDefCls.def(py::init<>())
        .def_readwrite("n_emitter", &b2LinearEmitterArrayDef::n_emitter)
        .def_readwrite("length", &b2LinearEmitterArrayDef::length)
        .def_readwrite("velocity", &b2LinearEmitterArrayDef::velocity)
    ;
    py::class_<b2LinearEmitterArray> lineEmitterCls(pybox2dModule, "LinearEmitterArray", emitterBaseCls);
    lineEmitterCls.def(py::init<b2ParticleSystem *, const b2LinearEmitterArrayDef &>())
        .def("step", &b2LinearEmitterArray::Step);



    // RANDOMIZED LINEAR
    py::class_<b2RandomizedLinearEmitterDef> randomizedLinearEmitterDefCls(pybox2dModule, "RandomizedLinearEmitterDef", emitterDefBaseCls);
    randomizedLinearEmitterDefCls.def(py::init<>())
        .def_readwrite("size", &b2RandomizedLinearEmitterDef::size)
        .def_readwrite("velocity", &b2RandomizedLinearEmitterDef::velocity)
    ;
    py::class_<b2RandomizedLinearEmitter> randomizedLinearEmitterCls(pybox2dModule, "RandomizedLinearEmitter", emitterBaseCls);
    randomizedLinearEmitterCls.def(py::init<b2ParticleSystem *, const b2RandomizedLinearEmitterDef &>())
        .def("step", &b2RandomizedLinearEmitter::Step);


    // RANDOMIZED RADIAL
    py::class_<b2RandomizedRadialEmitterDef> radialEmitterDefCls(pybox2dModule, "RandomizedRadialEmitterDef", emitterDefBaseCls);
    radialEmitterDefCls.def(py::init<>())
        .def_readwrite("inner_radius", &b2RandomizedRadialEmitterDef::innerRadius)
        .def_readwrite("outer_radius", &b2RandomizedRadialEmitterDef::outerRadius)
        .def_readwrite("velocity_magnitude",&b2RandomizedRadialEmitterDef::velocityMagnitude)
        .def_readwrite("start_angle", &b2RandomizedRadialEmitterDef::startAngle)
        .def_readwrite("stop_angle", &b2RandomizedRadialEmitterDef::stopAngle)
    ;

    py::class_<b2RandomizedRadialEmitter> radialEmitterCls(pybox2dModule, "RandomizedRadialEmitter",emitterBaseCls);
    radialEmitterCls
        .def(py::init<b2ParticleSystem *, const b2RandomizedRadialEmitterDef &>())
        .def("step", &b2RandomizedRadialEmitter::Step);
}
