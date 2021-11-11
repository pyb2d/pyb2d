#ifndef PYBOX2D_HELPER_HXX

#include <pybind11/pybind11.h>            // Pybind11 import to define Python bindings
#include <xtensor-python/pytensor.hpp>     // Numpy bindings
#include <xtensor/xtensor.hpp>    



using np_verts_row_major = xt::pytensor<float, 2, xt::layout_type::row_major>;
using np_verts_dynamic = xt::pytensor<float, 2, xt::layout_type::dynamic>;

template<class F>
void with_vertices(
    const np_verts_row_major & verts, F && f)
{
    if(verts.shape()[1] != 2)
    {
        throw std::runtime_error("wrong shape: needs to be [X,2]");
    }

    const b2Vec2 * ptr = reinterpret_cast<const b2Vec2 *>(verts.data());
    f(ptr, verts.shape()[0]);
}



template<class F>
void with_vertices(
    const np_verts_dynamic & verts, F && f)
{
    if(verts.shape()[1] != 2)
    {
        throw std::runtime_error("wrong shape: needs to be [X,2]");
    }

    xt::xtensor<float, 2, xt::layout_type::row_major> copy_verts(verts);
    const b2Vec2 * ptr = reinterpret_cast<const b2Vec2 *>(copy_verts.data());
    f(ptr, copy_verts.shape()[0]);

    
}

#endif