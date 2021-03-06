#ifndef PYB2D_HELPER_HXX
#define PYB2D_HELPER_HXX

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>            // Pybind11 import to define Python bindings
// #include <xtensor-python/pytensor.hpp>     // Numpy bindings
// #include <xtensor/xtensor.hpp>

#include "numpy.hxx"

using np_verts_row_major = py::array_t<float, py::array::c_style | py::array::forcecast>;
using np_vec2_row_major = py::array_t<float, py::array::c_style | py::array::forcecast>;

template<class T>
using cstyle_array = py::array_t<T, py::array::c_style | py::array::forcecast>;


template<class F>
void with_vertices(
    const np_verts_row_major & verts, F && f
)
{
    py::buffer_info buf = verts.request();

    auto verts2d = verts.unchecked<2>();
    if(verts2d.shape(1) != 2)
    {
        throw std::runtime_error("wrong shape: needs to be [X,2]");
    }

    auto ptr = reinterpret_cast<b2Vec2 *>(buf.ptr);
    f(ptr, std::size_t(verts2d.shape(0)));
}


template<class F>
void with_vec2_array(
    const np_vec2_row_major & verts, F && f
)
{
    py::buffer_info buf = verts.request();

    auto verts2d = verts.unchecked<2>();
    if(verts2d.shape(1) != 2)
    {
        throw std::runtime_error("wrong shape: needs to be [X,2]");
    }

    auto ptr = reinterpret_cast<b2Vec2 *>(buf.ptr);
    f(ptr, std::size_t(verts2d.shape(0)));
}





#endif
