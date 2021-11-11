#include <pybind11/pybind11.h>

namespace py = pybind11;
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
void exportB2Particle(py::module & );
void exportB2ParticleSystem(py::module & );
void exportB2ParticleGroup(py::module & );
void exportb2Collision(py::module & );
void exportExtendedDebugDraw(py::module & );

void exportb2Vectorization(py::module &);
void exportEmitter(py::module &);

PYBIND11_PLUGIN(_pybox2d) {
    py::module pybox2dModule("_pybox2d", "pybox2d python bindings");

    exportContact(pybox2dModule);
    exportB2World(pybox2dModule);
    exportB2Body(pybox2dModule);
    exportB2Math(pybox2dModule);
    exportB2Shape(pybox2dModule);
    exportB2Fixture(pybox2dModule);
    exportb2Joint(pybox2dModule);
    exportb2JointDef(pybox2dModule);
    exportB2WorldCallbacks(pybox2dModule);
    exportB2Draw(pybox2dModule);
    exportB2Particle(pybox2dModule);
    exportB2ParticleSystem(pybox2dModule);
    exportB2ParticleGroup(pybox2dModule);
    exportb2Collision(pybox2dModule);
    exportExtendedDebugDraw(pybox2dModule);
    exportb2Vectorization(pybox2dModule);
    exportEmitter(pybox2dModule);

    
    return pybox2dModule.ptr();
}
