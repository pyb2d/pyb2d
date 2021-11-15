#ifndef PYBOX2D_BATCH_DEBUG_DRAW_CALLER_OLD
#define PYBOX2D_BATCH_DEBUG_DRAW_CALLER_OLD

#include <pybind11/pybind11.h>
#include "../box2d_wrapper.hpp"

#include "../extensions/pyworld.hxx"

template<class T>
struct Vertices
{


    void add_polygon(const b2Vec2 * points, const std::size_t num_points)
    {   
        std::array<float, 2> p;
        p[0] = points[0].x;
        p[1] = points[0].y;
        m_points.push_back(p);
        m_connect.push_back(0);
        for(std::size_t i=0; i<num_points; ++i)
        {
            
            p[0] = points[i].x;
            p[1] = points[i].y;
            m_points.push_back(p);
            m_connect.push_back(1);
        } 

        p[0] = points[0].x;
        p[1] = points[0].y;

        m_points.push_back(p);
        m_connect.push_back(1);
        m_points.push_back(p);
        m_connect.push_back(0);

    }   

    void add_chain(const b2Vec2 * points, const std::size_t num_points)
    {   
        std::array<float, 2> p;
        for(std::size_t i=0; i<num_points; ++i)
        {
            
            p[0] = points[i].x;
            p[1] = points[i].y;
            m_points.push_back(p);
            m_connect.push_back(1);
            if(i + 1 == num_points)
            {
                m_points.push_back(p);
                m_connect.push_back(0);
            }
        } 


    }  
    void clear()
    {
        m_points.clear();
        m_connect.clear();
    }

    std::vector<std::array<float, 2>> m_points;
    std::vector<uint8_t> m_connect;
};

struct BatchDebugDrawOptions
{
    BatchDebugDrawOptions(){
        draw_shapes = true;
        draw_aabbs = true;
        draw_joints = true;
        draw_coms = true;
        #ifdef PYBOX2D_LIQUID_FUN
        draw_particles = true;
        #endif
        draw_circles_as_polygons = false;
        n_circle_vertices = 40;
    }

    bool draw_shapes;
    bool draw_aabbs;
    bool draw_joints;
    bool draw_coms;
    #ifdef PYBOX2D_LIQUID_FUN
    bool draw_particles;
    #endif
    bool draw_circles_as_polygons;
    int  n_circle_vertices;
};

const static uint8_t INACTIVE_BODY = 0;
const static uint8_t STATIC_BODY = 1;
const static uint8_t KINEMATIC_BODY = 2;
const static uint8_t SLEEPING_BODY = 3;
const static uint8_t DYNAMIC_BODY = 4;


template<class CONTAINER>
struct ShapeStorage
: public std::tuple
<
    CONTAINER,
    CONTAINER,
    CONTAINER,
    CONTAINER,
    CONTAINER
>
{
    void clear()
    {
        std::get<0>(*this).clear();
        std::get<1>(*this).clear();
        std::get<2>(*this).clear();
        std::get<3>(*this).clear();
        std::get<4>(*this).clear();
    }
};

std::vector<b2Vec2> make_circle_verts(const std::size_t num_verts)
{
    std::vector<b2Vec2> ret;
    const float angle_per_segment = (2.0*M_PI) / num_verts;
    for(std::size_t i=0; i<num_verts; ++i)
    {
        const float phi = angle_per_segment * static_cast<float>(i);
        ret.push_back(b2Vec2(std::cos(phi), std::sin(phi)));
    }
    return ret;
}


struct BatchDebugDrawCollector
{
    BatchDebugDrawCollector(const BatchDebugDrawOptions & options)
    :   m_options(options),
        m_standart_circle_verts(make_circle_verts(options.n_circle_vertices)),
        m_circle_verts(options.n_circle_vertices)
    {
    }

    void change_options(const BatchDebugDrawOptions & options)
    {
        m_options = options;
        if( m_standart_circle_verts.size() != options.n_circle_vertices)
        {
            m_standart_circle_verts = make_circle_verts(options.n_circle_vertices);
            m_circle_verts.resize(options.n_circle_vertices);
        }
    }

    typedef b2Vec2        Point2;
    typedef std::pair<Point2, Point2>   Point2Pair;

    struct Circle
    {
        Point2 center;
        Point2 axis;
        float  radius;
    };

    struct Edge
    {
        Point2 v1;
        Point2 v2;
    };

    struct BoundingBox
    {
        Point2 lower_bound;
        Point2 upper_bound;
    };


    // struct ParticleSystem
    // {

    // };

    void collect(PyWorld * world)
    {
        if(m_options.draw_shapes)
        {
            this->collect_shapes(world);
        }

        if(m_options.draw_joints)
        {
            for ( b2Joint* j = world->GetJointList(); j; j = j->GetNext())
            {
                this->collect_joint(j);
            }
        }

        if(m_options.draw_aabbs)
        {
            this->collect_aabbs(world);
        }

        if(m_options.draw_coms)
        {    
        }
        #ifdef PYBOX2D_LIQUID_FUN
        for (b2ParticleSystem* p = world->GetParticleSystemList(); p; p = p->GetNext())
        {
            collect_particle_system(p);
        }
        #endif
    }
    void collect_aabbs(b2World *world)
    {   
        //b2Color color(0.9f, 0.3f, 0.9f);
        const b2BroadPhase* bp = &world->GetContactManager().m_broadPhase;

        for ( b2Body* b = world->GetBodyList(); b; b = b->GetNext())
        {   
            #if PYBOX2D_OLD_BOX2D
            if (b->IsActive() == false)
            #else
            if (b->IsEnabled() == false)
            #endif
            {
                continue;
            }

            // for (b2Fixture* f = b->GetFixtureList(); f; f = f->GetNext())
            // {
            //     for (int32 i = 0; i < f->GetProxyCount(); ++i)
            //     {
            //         const b2FixtureProxy* proxy = f->GetProxies() + i;
            //         b2AABB aabb = bp->GetFatAABB(proxy->proxyId);
            //         b2Vec2 vs[4];
            //         vs[0].Set(aabb.lowerBound.x, aabb.lowerBound.y);
            //         vs[1].Set(aabb.upperBound.x, aabb.lowerBound.y);
            //         vs[2].Set(aabb.upperBound.x, aabb.upperBound.y);
            //         vs[3].Set(aabb.lowerBound.x, aabb.upperBound.y);

            //         for(std::size_t vi=0; vi<4; ++vi)
            //         {
            //             this->update_bounding_box(vs[vi]);
            //         }

            //         m_bounding_boxes.add_polygon(vs, 4);
            //         //m_debugDraw->DrawPolygon(vs, 4, color);
            //     }
            // }
        }
    }

    void collect_shapes(b2World * world)
    {
        if(m_options.draw_shapes)
        {
            for ( b2Body* b = world->GetBodyList(); b; b = b->GetNext())
            {
                const b2Transform& xf = b->GetTransform();
                for (b2Fixture* f = b->GetFixtureList(); f; f = f->GetNext())
                {
                    #if PYBOX2D_OLD_BOX2D
                    if (b->IsActive() == false)
                    #else
                    if (b->IsEnabled() == false)
                    #endif
                    {
                        this->collect_shape<INACTIVE_BODY>(f, xf);
                    }
                    else if (b->GetType() == b2_staticBody)
                    {
                        this->collect_shape<STATIC_BODY>(f, xf);
                    }
                    else if (b->GetType() == b2_kinematicBody)
                    {
                        this->collect_shape<KINEMATIC_BODY>(f, xf);
                    }
                    else if (b->IsAwake() == false)
                    {
                        this->collect_shape<SLEEPING_BODY>(f, xf);
                    }
                    else
                    {
                        this->collect_shape<DYNAMIC_BODY>(f, xf);
                    }
                }
            }
        }
    }

    template<uint8_t BODY_COLOR_TYPE>
    void collect_shape( b2Fixture* fixture, const b2Transform& xf)
    {
        auto & polygon_shapes = std::get<BODY_COLOR_TYPE>(m_polygon_shapes);
        auto & chain_shapes = std::get<BODY_COLOR_TYPE>(m_chain_shapes);

        switch (fixture->GetType())
        {
            case b2Shape::e_circle:
            {
                b2CircleShape* circle = (b2CircleShape*)fixture->GetShape();

                b2Vec2 center = b2Mul(xf, circle->m_p);
                float radius = circle->m_radius;
                b2Vec2 axis = b2Mul(xf.q, b2Vec2(1.0f, 0.0f));


                this->update_bounding_box(b2Vec2(center.x + radius, center.y +radius));
                this->update_bounding_box(b2Vec2(center.x - radius, center.y -radius));

                this->collect_circle_shape <BODY_COLOR_TYPE> (radius, center, axis);
                //m_debugDraw->DrawSolidCircle(center, radius, axis, color);
            }
            break;

            case b2Shape::e_edge:
            {
                b2EdgeShape* edge = (b2EdgeShape*)fixture->GetShape();
                b2Vec2 verts[2] = {
                    b2Mul(xf, edge->m_vertex1),
                    b2Mul(xf, edge->m_vertex2)
                };
                this->update_bounding_box(verts[0]);
                this->update_bounding_box(verts[1]);
                chain_shapes.add_chain(verts, 2);
            }
            break;

            case b2Shape::e_chain:
            {
                // todo avoid buffer...
                b2ChainShape* chain = (b2ChainShape*)fixture->GetShape();
                int32 count = chain->m_count;
                if(count < b2_maxPolygonVertices)
                {
                    b2Vec2 vertices[b2_maxPolygonVertices];
                    for (int32 i = 0; i < count; ++i)
                    {
                        vertices[i] = b2Mul(xf, chain->m_vertices[i]);
                        this->update_bounding_box(vertices[i]);
                    }
                    chain_shapes.add_chain(vertices, count);
                }
                else{
                    std::vector<b2Vec2> vertices(count);
                    for (int32 i = 0; i < count; ++i)
                    {
                        vertices[i] = b2Mul(xf, chain->m_vertices[i]);
                        this->update_bounding_box(vertices[i]);
                    }
                    chain_shapes.add_chain(vertices.data(), count);
                }


            }
            break;

            case b2Shape::e_polygon:
            {
                b2PolygonShape* poly = (b2PolygonShape*)fixture->GetShape();
                int32 vertexCount = poly->m_count;
                b2Assert(vertexCount <= b2_maxPolygonVertices);
                b2Vec2 vertices[b2_maxPolygonVertices];

                for (int32 i = 0; i < vertexCount; ++i)
                {
                    vertices[i] = b2Mul(xf, poly->m_vertices[i]);
                    this->update_bounding_box(vertices[i]);
                }
                polygon_shapes.add_polygon(vertices, vertexCount);
                //m_debugDraw->DrawSolidPolygon(vertices, vertexCount, color);
            }
            break;

            default:
                break;
        }
    }

    template<uint8_t BODY_COLOR_TYPE>
    void collect_circle_shape(const float radius, const b2Vec2 & center, b2Vec2 axis)
    {

        auto & polygon_shapes = std::get<BODY_COLOR_TYPE>(m_polygon_shapes);
        for(std::size_t i=0; i<m_standart_circle_verts.size(); ++i)
        {
            m_circle_verts[i] = b2Vec2(m_standart_circle_verts[i].x *radius + center.x,
                                       m_standart_circle_verts[i].y *radius + center.y);
                
        }
        polygon_shapes.add_polygon(m_circle_verts.data(), m_circle_verts.size());

        axis *= radius;
        axis += center;
        m_circles_axis.push_back(center);
        m_circles_axis.push_back(axis);
    }

    void collect_joint( b2Joint * joint)
    {
        b2Body* bodyA = joint->GetBodyA();
        b2Body* bodyB = joint->GetBodyB();
        const b2Transform& xf1 = bodyA->GetTransform();
        const b2Transform& xf2 = bodyB->GetTransform();
        b2Vec2 x1 = xf1.p;
        b2Vec2 x2 = xf2.p;
        b2Vec2 p1 = joint->GetAnchorA();
        b2Vec2 p2 = joint->GetAnchorB();

        b2Color color(0.5f, 0.8f, 0.8f);

        switch (joint->GetType())
        {
            case e_distanceJoint:
            {
                this->collect_joint_segments(p1, p2);
            }
            break;

            case e_pulleyJoint:
            {
                b2PulleyJoint* pulley = (b2PulleyJoint*)joint;
                b2Vec2 s1 = pulley->GetGroundAnchorA();
                b2Vec2 s2 = pulley->GetGroundAnchorB();
                this->collect_joint_segments(s1, p1);
                this->collect_joint_segments(s2, p2);
                this->collect_joint_segments(s1, s2);

                

            }
            break;

            case e_mouseJoint:
            {
                // don't draw this
                
            }
            break;

            default:
            {
                this->collect_joint_segments(x1, p1);
                this->collect_joint_segments(p1, p2);
                this->collect_joint_segments(x2, p2);
            }
            break;

        }
    }
    void collect_joint_segments(const b2Vec2 & a, const b2Vec2 & b)
    {
        if(
            std::isfinite(a.x) && std::isfinite(a.y) &&
            std::isfinite(b.x) && std::isfinite(b.y) &&
            b2Distance(a,b) > 0.0000001
        ){

            this->update_bounding_box(a);
            this->update_bounding_box(b);
            m_joint_segments.push_back(Point2Pair(a,b));
        }
    }   
    #ifdef PYBOX2D_LIQUID_FUN
    void collect_particle_system(const b2ParticleSystem * system)
    {
        int32 particleCount = system->GetParticleCount();
        const b2Vec2* positionBuffer = system->GetPositionBuffer();
        for(int32 pi=0; pi<particleCount; ++pi)
        {
            this->update_bounding_box(positionBuffer[pi]);
        }
        m_particle_systems.push_back(system);
    }
    #endif
    void clear()
    {
        m_joint_segments.clear();
        m_body_types.clear();
        m_center_of_mass_vector.clear();
        m_circle_shapes.clear();
        m_edge_shapes.clear();
        m_chain_shapes.clear();
        m_polygon_shapes.clear();
        m_bounding_boxes.clear();
        m_circles_axis.clear();
        #ifdef PYBOX2D_LIQUID_FUN
        m_particle_systems.clear();
        #endif
        
        m_drawing_bounding_box.lowerBound.x = std::numeric_limits<float>::infinity();
        m_drawing_bounding_box.lowerBound.y = std::numeric_limits<float>::infinity();

        m_drawing_bounding_box.upperBound.x = -1.0 * std::numeric_limits<float>::infinity();
        m_drawing_bounding_box.upperBound.y = -1.0 * std::numeric_limits<float>::infinity();
    }

    void update_bounding_box(const b2Vec2 & p)
    {
        m_drawing_bounding_box.lowerBound.x = std::min(m_drawing_bounding_box.lowerBound.x, p.x);
        m_drawing_bounding_box.lowerBound.y = std::min(m_drawing_bounding_box.lowerBound.y, p.y);
        m_drawing_bounding_box.upperBound.x = std::max(m_drawing_bounding_box.upperBound.x, p.x);
        m_drawing_bounding_box.upperBound.y = std::max(m_drawing_bounding_box.upperBound.y, p.y);
    }


    BatchDebugDrawOptions m_options;

    // the drawing bb
    b2AABB m_drawing_bounding_box;

    // joints
    std::vector<Point2Pair > m_joint_segments;



    // bodies
    std::vector<uint8_t >    m_body_types;
    std::vector<Point2>      m_center_of_mass_vector;
    

    // shapes
    ShapeStorage<std::vector<Circle>> m_circle_shapes;
    ShapeStorage<std::vector<Edge>>   m_edge_shapes;
    ShapeStorage<Vertices<float>>     m_chain_shapes;
    ShapeStorage<Vertices<float>>     m_polygon_shapes;
    Vertices<float>                   m_bounding_boxes;

    // circle axis
    std::vector<Point2>               m_circles_axis;

    // standart circle
    std::vector<b2Vec2> m_standart_circle_verts;
    std::vector<b2Vec2> m_circle_verts;

    #ifdef PYBOX2D_LIQUID_FUN
    // particle systems
    std::vector<const b2ParticleSystem * > m_particle_systems;
    #endif
};

#endif