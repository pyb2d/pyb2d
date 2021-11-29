#pragma once
namespace py = pybind11;

#include "../helper.hxx"

template<class CLS, class PY_CLS>
void add_debug_draw_api(PY_CLS & py_cls)
{
    py_cls

        // draw from python
        .def("draw_point",         &CLS::DrawPoint)
        .def("draw_circle",        &CLS::DrawCircle)
        .def("draw_solid_circle",  &CLS::DrawSolidCircle)
        .def("draw_segment",       &CLS::DrawSegment)

        .def("draw_polygon", [](CLS * self, const np_verts_row_major & verts, const b2Color& color)
        {
            with_vertices(verts, [&](auto ptr, auto n_verts)
            {
                self->DrawPolygon(ptr, n_verts, color);
            });
        })
        .def("draw_solid_polygon", [](CLS * self, const np_verts_row_major & verts, const b2Color& color)
        {
            with_vertices(verts, [&](auto ptr, auto n_verts)
            {
                self->DrawSolidPolygon(ptr, n_verts, color);
            });
        })

        .def("_append_flags_int",[](CLS * draw,const int flag){draw->AppendFlags(flag);})
        .def("_clear_flags_int",[](CLS * draw,const int flag){draw->ClearFlags(flag);})

    ;
}  


template<class CLS, class PY_CLS>
void add_debug_draw_transform_api(PY_CLS & py_cls)
{
    py_cls

        // convert screen to world / world to screen
        .def("world_to_screen", &CLS::world_to_screen)
        .def("screen_to_world", &CLS::screen_to_world)
        .def("world_to_screen_scale", &CLS::world_to_screen_scale)
        .def("screen_to_world_scale", &CLS::screen_to_world_scale)

        // get the scale
        .def_readwrite("screen_size",&CLS::m_screen_size)
        .def_readwrite("scale",&CLS::m_scale)
        .def_readwrite("translate",&CLS::m_translate)
        .def_readwrite("flip_y",&CLS::m_flip_y)
    ;
}  