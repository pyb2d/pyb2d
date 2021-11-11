#pragma once
#include <box2d/box2d.h>

#include <pybind11/pybind11.h>
#include "pyb2WorldCallbacks.hxx"
#include <memory>

#include "user_data.hxx"





class PyWorld : public b2World
{
public:
    PyWorld(const b2Vec2& gravity)
    :   b2World(gravity),
        m_destruction_listener(new PyWorldDestructionListenerCaller())
    {
        // install destruction listener
        this->SetDestructionListener(m_destruction_listener.get());
    }
    ~PyWorld(){
        for ( b2Body* b = this->GetBodyList(); b; b = b->GetNext())
        {
            delete_user_data_if_has_user_data(b);
        }
    }

    void set_py_destruction_listener(const py::object & object)
    {
        this->m_destruction_listener->set_py_destruction_listener(object);
    }


private:
    std::unique_ptr<PyWorldDestructionListenerCaller> m_destruction_listener;
};