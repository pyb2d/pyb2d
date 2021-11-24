#pragma once
#include "../box2d_wrapper.hpp"
#include <pybind11/pybind11.h>
#include "../pyb2WorldCallbacks.hxx"
#include <memory>
#include "../debug_draw/extended_debug_draw_base.hxx"



class PyWorld : public b2World
{
public:
    PyWorld(const b2Vec2& gravity)
    :   b2World(gravity),
        m_destruction_listener(new PyWorldDestructionListenerCaller()),
        p_extended_debug_draw(nullptr)
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

    void SetExtendedDebugDraw(ExtendedDebugDrawBase * extended_debug_draw)
    {   
        if(p_extended_debug_draw)
        {
            throw std::runtime_error("PyWorld has already a debug draw");
        }
        this->SetDebugDraw(extended_debug_draw);
        p_extended_debug_draw = extended_debug_draw;
    }
    #if PYBOX2D_OLD_BOX2D
    void DebugDraw(){
        return this->DrawDebugData();
    }
    #endif

    void ExtendedDebugDraw(const py::object & object)
    {
        bool has_pre_debug_draw = py::hasattr(object, "pre_debug_draw");
        bool has_post_debug_draw = py::hasattr(object, "post_debug_draw");

        if(p_extended_debug_draw){
            p_extended_debug_draw->BeginDraw();
            if(has_pre_debug_draw)
            {
                object.attr("pre_debug_draw")();
            }

            // 
            if(p_extended_debug_draw->ReleaseGilWhileDebugDraw())
            {
                py::gil_scoped_release release;
                this->DebugDraw();
            }
            else
            {
                this->DebugDraw();
            }

            if(has_post_debug_draw)
            {
                object.attr("post_debug_draw")();
            }

            p_extended_debug_draw->EndDraw();
        }
    }


    std::pair<b2Vec2,b2Vec2> aabb()
    {
        b2Vec2  lower( std::numeric_limits<float>::infinity(),    
                       std::numeric_limits<float>::infinity());
        b2Vec2  upper(-std::numeric_limits<float>::infinity(),
                      -std::numeric_limits<float>::infinity());

        auto update_aabb = [&](const b2Vec2 & p)
        {
            lower.x = std::min(lower.x, p.x);
            lower.y = std::min(lower.y, p.y);

            upper.x = std::max(upper.x, p.x);
            upper.y = std::max(upper.y, p.y);
        };

        for (b2Body* b = GetBodyList(); b; b = b->GetNext())
        {
            const b2Transform& xf = b->GetTransform();
            for (b2Fixture* fixture = b->GetFixtureList(); fixture; fixture = fixture->GetNext())
            {
                switch (fixture->GetType())
                {
                    case b2Shape::e_circle:
                    {
                        b2CircleShape* circle = (b2CircleShape*)fixture->GetShape();

                        b2Vec2 center = b2Mul(xf, circle->m_p);
                        const float radius = circle->m_radius;
                        update_aabb(b2Vec2(center.x + radius, center.y + radius));
                        update_aabb(b2Vec2(center.x - radius, center.y - radius));
                    }
                    break;

                    case b2Shape::e_edge:
                    {
                        b2EdgeShape* edge = (b2EdgeShape*)fixture->GetShape();
                        b2Vec2 v1 = b2Mul(xf, edge->m_vertex1);
                        b2Vec2 v2 = b2Mul(xf, edge->m_vertex2);
                        update_aabb(v1);
                        update_aabb(v2);
                        
                    }
                    break;

                    case b2Shape::e_chain:
                    {
                        b2ChainShape* chain = (b2ChainShape*)fixture->GetShape();
                        int32 count = chain->m_count;
                        const b2Vec2* vertices = chain->m_vertices;

                        for (int32 i = 0; i < count; ++i)
                        {
                            update_aabb(b2Mul(xf, vertices[i]));
                        }
                    }
                    break;

                    case b2Shape::e_polygon:
                    {
                        b2PolygonShape* poly = (b2PolygonShape*)fixture->GetShape();
                        int32 vertexCount = poly->m_count;
                        b2Vec2 vertices[b2_maxPolygonVertices];

                        for (int32 i = 0; i < vertexCount; ++i)
                        {
                            update_aabb(b2Mul(xf, poly->m_vertices[i]));
                        }

                    }
                    break;

                    default:
                        break;
                }
            }
        }
        return std::make_pair(lower, upper);
    }


private:
    std::unique_ptr<PyWorldDestructionListenerCaller> m_destruction_listener;
    ExtendedDebugDrawBase  * p_extended_debug_draw;
};