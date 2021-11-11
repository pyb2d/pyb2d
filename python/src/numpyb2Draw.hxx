#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <box2d/box2d.h>

#include <iostream>

namespace py = pybind11;


class PyB2Draw : public b2Draw {
public:

    typedef std::pair<float,float> P;
    typedef std::tuple<float,float,float> C;

    /* Inherit the constructors */
    //using b2Draw::b2Draw;

    virtual ~PyB2Draw() {}

    PyB2Draw(
        const py::object object
    )
    :   object_(object){

    }


    virtual void DrawPolygon(const b2Vec2* vertices, int32 vertexCount, const b2Color& color) {
        
        //typedef long unsigned int ShapeType;

        auto npVertices = py::array(py::buffer_info(
            nullptr,            /* Pointer to data (nullptr -> ask NumPy to allocate!) */
            sizeof(float),     /* Size of one item */
            py::format_descriptor<float>::value, /* Buffer format */
            2,          /* How many dimensions? */
            { size_t(vertexCount), size_t(2) },  /* Number of elements for each dimension */
            { 2*sizeof(float),sizeof(float)}  /* Strides for each dimension */
        ));

        float * ptr  = static_cast<float* >(npVertices.request().ptr);        
        for(size_t i=0;  i<size_t(vertexCount); ++i){
            auto v = vertices[i];
            ptr[i*2 ]   = v.x;
            ptr[i*2 +1] = v.y;
        }
        py::object f = object_.attr("draw_polygon");
        f(npVertices,C(color.r,color.g,color.b));
    }

    virtual void DrawSolidPolygon(const b2Vec2* vertices, int32 vertexCount, const b2Color& color) {
        auto npVertices = py::array(py::buffer_info(
            nullptr,            /* Pointer to data (nullptr -> ask NumPy to allocate!) */
            sizeof(float),     /* Size of one item */
            py::format_descriptor<float>::value, /* Buffer format */
            2,          /* How many dimensions? */
            { size_t(vertexCount), size_t(2) },  /* Number of elements for each dimension */
            { 2*sizeof(float),sizeof(float)}  /* Strides for each dimension */
        ));

        float * ptr  = static_cast<float* >(npVertices.request().ptr);        
        for(size_t i=0;  i<size_t(vertexCount); ++i){
            auto v = vertices[i];
            ptr[i*2 ]   = v.x;
            ptr[i*2 +1] = v.y;
        }
        py::object f = object_.attr("draw_solid_polygon");
        f(npVertices,C(color.r,color.g,color.b));
    }

    virtual void DrawCircle(const b2Vec2& center, float radius, const b2Color& color) {
        py::object f = object_.attr("draw_circle");
        auto c =center;
        f(P(c.x,c.y),radius,C(color.r,color.g,color.b));
    }

    virtual void DrawSolidCircle(const b2Vec2& center, float radius, const b2Vec2& axis, const b2Color& color) {
        py::object f = object_.attr("draw_solid_circle");
        auto c = center;
        f(P(c.x,c.y),radius,P(axis.x,axis.y), C(color.r,color.g,color.b));
    }

    virtual void DrawParticles(const b2Vec2 *centers, float radius, const b2ParticleColor *colors, const int32 count) {
        py::object f = object_.attr("draw_particles");

        auto npCenters = py::array(py::buffer_info(
            nullptr,            /* Pointer to data (nullptr -> ask NumPy to allocate!) */
            sizeof(float),     /* Size of one item */
            py::format_descriptor<float>::value, /* Buffer format */
            2,          /* How many dimensions? */
            { size_t(count), size_t(2) },  /* Number of elements for each dimension */
            { 2*sizeof(float),sizeof(float)}  /* Strides for each dimension */
        ));

        

        float * ptrCenters  = static_cast<float* >(npCenters.request().ptr);
        if(colors != nullptr){
            auto npColors = py::array(py::buffer_info(
                nullptr,            /* Pointer to data (nullptr -> ask NumPy to allocate!) */
                sizeof(uint8),     /* Size of one item */
                py::format_descriptor<uint8>::value, /* Buffer format */
                2,          /* How many dimensions? */
                { size_t(count), size_t(4) },  /* Number of elements for each dimension */
                { 4*sizeof(uint8),sizeof(uint8)}  /* Strides for each dimension */
            ));
            uint8 * ptrColors  = static_cast<uint8 * >(npColors.request().ptr);

            for(size_t i=0;  i<size_t(count); ++i){
                auto ce = centers[i];
                ptrCenters[i*2 ]   = ce.x ;
                ptrCenters[i*2 +1] = ce.y ; 
                const b2ParticleColor c = colors[i];
                ptrColors[i*4 ]   = c.r;
                ptrColors[i*4 +1] = c.g;
                ptrColors[i*4 +2] = c.b;
                ptrColors[i*4 +3] = c.a;
            }
            f(npCenters,radius,npColors);
        }
        else{
            for(size_t i=0;  i<size_t(count); ++i){
                auto ce = centers[i];
                ptrCenters[i*2 ]   = ce.x ;
                ptrCenters[i*2 +1] = ce.y ; 
            }
            f(npCenters,radius);
        }
    }

    virtual void DrawSegment(const b2Vec2& p1, const b2Vec2& p2, const b2Color& color) {
        py::object f = object_.attr("draw_segment");
        auto pp1 =  p1;
        auto pp2 =  p2;
        f(P(pp1.x,pp1.y),P(pp2.x,pp2.y),C(color.r,color.g,color.b));
    }

    virtual void DrawTransform(const b2Transform& xf) {
       transform_ = xf;
       //py::object f = object_.attr("DrawTransform");
       //f(xf);
    }

    b2Transform transform_;

    py::object object_;
};
