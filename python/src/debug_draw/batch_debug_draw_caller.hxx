#ifndef PYBOX2D_BATCH_DEBUG_DRAW_CALLER
#define PYBOX2D_BATCH_DEBUG_DRAW_CALLER
#include "../numpy.hxx"

#include "extended_debug_draw_base.hxx"

// the RoundingHelper class helps to generalize between floating
// point and non floating point coordinate value types.

template<class COORDINATE_VALUE_TYPE, bool IS_FLOAT = std::is_floating_point<COORDINATE_VALUE_TYPE>::value >
class RoundingHelper;


template<class COORDINATE_VALUE_TYPE>
class RoundingHelper<COORDINATE_VALUE_TYPE, true>
{
public:
    void round_and_add(const b2Vec2 & point, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        vec.push_back(point.x);
        vec.push_back(point.y);
    }
    void round_and_add(const float length, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        vec.push_back(length);
    }
};

template<class COORDINATE_VALUE_TYPE>
class RoundingHelper<COORDINATE_VALUE_TYPE, false>
{
public:
    void round_and_add(const b2Vec2 & point, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        vec.push_back(point.x + 0.5f);
        vec.push_back(point.y + 0.5f);
    }
    void round_and_add(const float length, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        vec.push_back(length + 0.5f);
    }
};






template<class COORDINATE_VALUE_TYPE, bool WITH_TRANSFORM>
class CoordinateHelper;


template<class COORDINATE_VALUE_TYPE>
class CoordinateHelper<COORDINATE_VALUE_TYPE, true> : public RoundingHelper<COORDINATE_VALUE_TYPE>
{
public:
    CoordinateHelper()
    :    
        m_screen_size{0,0},
        m_scale(1),
        m_translate(0,0),
        m_flip_y(true)
    {

    }

    b2Vec2 world_to_screen(const b2Vec2 & world_vec)const
    {   
        if(!m_flip_y)
        {

            return b2Vec2(
                world_vec.x * m_scale + m_translate.x,
                world_vec.y * m_scale + m_translate.y
            );
        }
        else
        {
            return b2Vec2(
                world_vec.x * m_scale + m_translate.x,
                m_screen_size[1] - world_vec.y * m_scale - m_translate.y
            );
        }
        
    }

    b2Vec2 screen_to_world(const b2Vec2 & screen_vec)const
    {   

        if(!m_flip_y)
        {

            return b2Vec2(
                (screen_vec.x  - m_translate.x) / m_scale,
                (screen_vec.y  - m_translate.y) / m_scale
            );
        }
        else
        {
            return b2Vec2(
                (screen_vec.x  - m_translate.x) / m_scale,
                (m_screen_size[1] - (screen_vec.y + m_translate.y) )/ m_scale
            );
        }
    }

    float world_to_screen_scale(const float d) const
    {
        return m_scale * d;
    }

    float screen_to_world_scale(const float d) const
    {
        return d/m_scale;
    }

    void add(const b2Vec2 & point, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        this->round_and_add(world_to_screen(point), vec);
    }
    void add(const float length, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        this->round_and_add(world_to_screen_scale(length), vec);
    }

public:
    std::array<std::size_t, 2> m_screen_size;
    float m_scale;
    b2Vec2 m_translate;
    bool m_flip_y;
};

template<class COORDINATE_VALUE_TYPE>
class CoordinateHelper<COORDINATE_VALUE_TYPE, false> : public RoundingHelper<COORDINATE_VALUE_TYPE>
{
public:
   
    void add(const b2Vec2 & point, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        this->round_and_add(point, vec);
    }
    void add(const float length, std::vector<COORDINATE_VALUE_TYPE> & vec)
    {
        this->round_and_add(length, vec);
    }
protected:
};




template<
    class COLOR_VALUE_TYPE,
    class COORDINATE_VALUE_TYPE,
    bool WITH_TRANSFORM
>
class BatchDebugDrawCallerBase : 
    public ExtendedDebugDrawBase, public CoordinateHelper<COORDINATE_VALUE_TYPE, WITH_TRANSFORM>
{
public:

    using color_value_type = COLOR_VALUE_TYPE;
    using color_vector_type = std::vector<color_value_type>;

    using coordinate_value_type = COORDINATE_VALUE_TYPE;
    using coordinate_vector_type = std::vector<coordinate_value_type>;


    virtual ~BatchDebugDrawCallerBase() {}

    BatchDebugDrawCallerBase(
        const py::object object
    )
    :   m_object(object)
    {

    }

    void BeginDraw() override {
        m_object.attr("begin_draw")();
    }

    void EndDraw() override {
        this->trigger_callbacks();
        m_object.attr("end_draw")();
    }
    
    bool ReleaseGilWhileDebugDraw() override {
        return true;
    }



    // virtual void DrawScreenText(
    //     const b2Vec  postion,
    //     const std::string & text,
    //     const float size,
    //     const b2Color & color
    // ){

    // }

    virtual void DrawPolygon(const b2Vec2* vertices, int32 vertexCount, const b2Color& color)
    {
        m_polygon_sizes.push_back(vertexCount);
        add_color(color, m_polygon_colors);
        for(std::size_t i=0; i<vertexCount; ++i)
        {
            this->add(vertices[i], m_polygon_verts);
        }
    }

    virtual void DrawSolidPolygon(const b2Vec2* vertices, int32 vertexCount, const b2Color& color)
    {
        m_solid_polygon_sizes.push_back(vertexCount);
        add_color(color, m_solid_polygon_colors);
        for(std::size_t i=0; i<vertexCount; ++i)
        {
            this->add(vertices[i], m_solid_polygon_verts);
        }
    }

    virtual void DrawPoint(const b2Vec2& center, float size, const b2Color& color) {
       this->add(center, m_point_coords);
       this->add(size, m_point_sizes);
       this->add_color(color, m_point_colors);
    }

    virtual void DrawCircle(const b2Vec2& center, float radius, const b2Color& color) {

        this->add(center, m_circle_coords);
        this->add(radius, m_circle_radii);
        add_color(color, m_circle_colors);
    }

    virtual void DrawSolidCircle(const b2Vec2& center, float radius, const b2Vec2& axis, const b2Color& color) {
        this->add(center, m_solid_circle_coords);
        this->add(radius, m_solid_circle_radii);
        m_solid_circle_axis.push_back(axis.x);
        m_solid_circle_axis.push_back(axis.y);
        this->add_color(color, m_solid_circle_colors);
    }


    virtual void DrawSegment(const b2Vec2& p1, const b2Vec2& p2, const b2Color& color) {

        this->add(p1, m_segment_coords);
        this->add(p2, m_segment_coords);
        this->add_color(color, m_segment_colors);
    }

    virtual void DrawTransform(const b2Transform& xf) {

    }

    #ifdef PYBOX2D_LIQUID_FUN
    virtual void DrawParticles(const b2Vec2 *centers, float radius, const b2ParticleColor *colors, const int32 count) {
        m_particle_systems_size.push_back(count);
        this->add(radius, m_particle_systems_radii);
        m_particle_systems_has_colors.push_back(colors != nullptr);

        for(int32 i=0; i<count; ++i)
        {
            this->add(centers[i], m_particle_systems_centers);

            if(colors != nullptr)
            {
                this->add_color(colors[i], m_particle_systems_colors);
            }
        }
    }
    #endif
    void trigger_callbacks(){


        #ifdef PYBOX2D_LIQUID_FUN
        //py::object f = m_object.attr("draw_particles");
        auto coord_offset = 0;
        auto color_offset = 0;
        for(auto psi=0; psi<m_particle_systems_radii.size(); ++psi)
        {
            const auto radius = m_particle_systems_radii[psi];
            const auto n_particels = m_particle_systems_size[psi];
            const auto has_colors = m_particle_systems_has_colors[psi];

            auto centers_ptr = m_particle_systems_centers.data() + coord_offset;

            if(!has_colors)
            {
                m_object.attr("_draw_particles")(
                    np_view(centers_ptr, {n_particels, 2}),
                    radius
                );
            } 
            else
            {
                auto color_ptr = m_particle_systems_colors.data() + color_offset;
                m_object.attr("_draw_particles")(
                    np_view(centers_ptr, {n_particels, 2}),
                    radius, 
                    np_view(color_ptr, {n_particels, 4})
                );
                color_offset += 4 * n_particels;
            }

            coord_offset += 2* n_particels;
        }
        #endif
        
        if(!m_solid_polygon_sizes.empty())
        {
            m_object.attr("_draw_solid_polygons")(
                np_view(m_solid_polygon_verts.data(),  {m_solid_polygon_verts.size()/2, std::size_t(2)}),
                np_view(m_solid_polygon_sizes.data(),  {m_solid_polygon_sizes.size()}),
                np_view(m_solid_polygon_colors.data(), {m_solid_polygon_colors.size()/3, 3})
            );
        }
        if(!m_solid_circle_coords.empty())
        {
            m_object.attr("_draw_solid_circles")(
                np_view(m_solid_circle_coords.data(), {m_solid_circle_coords.size()/2, std::size_t(2)}),
                np_view(m_solid_circle_radii.data(),  {m_solid_circle_radii.size()}),
                np_view(m_solid_circle_axis.data(),  {m_solid_circle_axis.size()/2, 2}),
                np_view(m_solid_circle_colors.data(), {m_solid_circle_colors.size()/3, 3})
            );
        }
        if(!m_polygon_sizes.empty())
        {
            m_object.attr("_draw_polygons")(
                np_view(m_polygon_verts.data(),  {m_polygon_verts.size()/2, std::size_t(2)}),
                np_view(m_polygon_sizes.data(),  {m_polygon_sizes.size()}),
                np_view(m_polygon_colors.data(), {m_polygon_colors.size()/3, 3})
            );
        }
        if(!m_circle_coords.empty())
        {
            m_object.attr("_draw_circles")(
                np_view(m_circle_coords.data(), {m_circle_coords.size()/2, std::size_t(2)}),
                np_view(m_circle_radii.data(),  {m_circle_radii.size()}),
                np_view(m_circle_colors.data(), {m_circle_colors.size()/3, 3})
            );
        }
        {
            py::object f = m_object.attr("_draw_points");
        }
        if(!m_segment_coords.empty())
        {

            m_object.attr("_draw_segments")(
                np_view(m_segment_coords.data(), {m_segment_coords.size()/4, std::size_t(2) ,std::size_t(2)}),
                np_view(m_segment_colors.data(), {m_segment_colors.size()/3, 3})
            );
        }


        this->reset();
    }
    void reset()
    {
        m_polygon_verts.resize(0);
        m_polygon_sizes.resize(0);
        m_polygon_colors.resize(0);
        m_solid_polygon_verts.resize(0);
        m_solid_polygon_sizes.resize(0);
        m_solid_circle_axis.resize(0);
        m_solid_polygon_colors.resize(0);
        m_circle_coords.resize(0);
        m_circle_radii.resize(0);
        m_circle_colors.resize(0);
        m_solid_circle_coords.resize(0);
        m_solid_circle_radii.resize(0);
        m_solid_circle_colors.resize(0);
        m_point_coords.resize(0);
        m_point_sizes.resize(0);
        m_point_colors.resize(0);
        m_segment_coords.resize(0);
        m_segment_colors.resize(0);
        #ifdef PYBOX2D_LIQUID_FUN
        m_particle_systems_centers.resize(0);
        m_particle_systems_size.resize(0);
        m_particle_systems_radii.resize(0);
        m_particle_systems_has_colors.resize(0);
        m_particle_systems_colors.resize(0);
        #endif
    }

    void add_color(const b2Color & color, std::vector<float> & color_array)
    {
        color_array.push_back(color.r);
        color_array.push_back(color.g);
        color_array.push_back(color.b);
    }
    void add_color(const b2Color & color, std::vector<uint8_t> & color_array)
    {
        color_array.push_back(uint8_t(color.r * 255.0 + 0.5));
        color_array.push_back(uint8_t(color.g * 255.0 + 0.5));
        color_array.push_back(uint8_t(color.b * 255.0 + 0.5));
    }
    #ifdef PYBOX2D_LIQUID_FUN
    void add_color(const b2ParticleColor & color, std::vector<float> & color_array)
    {
        color_array.push_back(float(color.r)/255.0f);
        color_array.push_back(float(color.g)/255.0f);
        color_array.push_back(float(color.b)/255.0f);
        color_array.push_back(float(color.a)/255.0f);
    }
    void add_color(const b2ParticleColor & color, std::vector<uint8_t> & color_array)
    {
        color_array.push_back(color.r);
        color_array.push_back(color.g);
        color_array.push_back(color.b);
        color_array.push_back(color.a);
    }
    #endif
    std::array<coordinate_value_type, 2> m_min_coord;
    std::array<coordinate_value_type, 2> m_max_coord;

    // polygon
    coordinate_vector_type      m_polygon_verts;
    std::vector<uint16_t>       m_polygon_sizes;
    color_vector_type           m_polygon_colors;

    // solid polygon
    coordinate_vector_type      m_solid_polygon_verts;
    std::vector<uint16_t>       m_solid_polygon_sizes;
    std::vector<float>          m_solid_circle_axis;
    color_vector_type           m_solid_polygon_colors;

    // circle
    coordinate_vector_type      m_circle_coords;
    coordinate_vector_type      m_circle_radii;
    color_vector_type           m_circle_colors;

    // solid circle
    coordinate_vector_type      m_solid_circle_coords;
    coordinate_vector_type      m_solid_circle_radii;
    color_vector_type           m_solid_circle_colors;  

    // points
    coordinate_vector_type      m_point_coords;
    coordinate_vector_type      m_point_sizes;
    color_vector_type           m_point_colors;

    // segments
    coordinate_vector_type      m_segment_coords;
    color_vector_type           m_segment_colors;

    #ifdef PYBOX2D_LIQUID_FUN

    // particles
    coordinate_vector_type      m_particle_systems_centers;
    std::vector<uint32_t>       m_particle_systems_size;
    coordinate_vector_type      m_particle_systems_radii;
    color_vector_type           m_particle_systems_has_colors;
    color_vector_type           m_particle_systems_colors;

    #endif


    py::object m_object;

public:

    // float m_scale;
    // b2Vec2 m_translate;
    // bool m_flip_y;

};


template<
    class COLOR_VALUE_TYPE,
    class COORDINATE_VALUE_TYPE,
    bool WITH_TRANSFORM
>
class BatchDebugDrawCaller : public BatchDebugDrawCallerBase<
    COLOR_VALUE_TYPE,COORDINATE_VALUE_TYPE,WITH_TRANSFORM
>{
    using base_type = BatchDebugDrawCallerBase<COLOR_VALUE_TYPE, COORDINATE_VALUE_TYPE, WITH_TRANSFORM>;
    using base_type::base_type;
};


#endif