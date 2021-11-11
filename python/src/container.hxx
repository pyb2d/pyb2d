#include <pybind11/pybind11.h>

#include <box2d/box2d.h>


#include "holder.hxx"


namespace py = pybind11;



template<class CONTAINER>
void make_container_cls_common(py::class_<CONTAINER> & py_class)
{
    typedef CONTAINER container_type;
    typedef typename CONTAINER::iterator iterator;
    typedef typename container_type::value_type ptr_type;
    typedef typename std::remove_pointer<ptr_type>::type value_type;
    typedef Holder<value_type> holder_type;

    py_class
        .def(py::init<>())
        .def("clear", &container_type::clear)
        .def("__len__", &container_type::size)
        .def("__iter__", [](container_type &v) {
            return py::make_iterator<
                py::return_value_policy::copy,
                iterator,
                iterator, 
                holder_type
            >(v.begin(), v.end());
        }, py::keep_alive<0, 1>()) /* Keep vector alive while iterator is used */
    ;
}


template<class CONTAINER>
void make_vector_cls(py::class_<CONTAINER> & py_class)
{
    typedef CONTAINER container_type;
    typedef typename CONTAINER::iterator iterator;
    typedef typename container_type::value_type ptr_type;
    typedef typename std::remove_pointer<ptr_type>::type value_type;
    typedef Holder<value_type> holder_type;

    // add iterator things
    make_container_cls_common(py_class);

    py_class
        .def("append", [](container_type &  self, ptr_type  val){
            self.push_back(val);
        })
        .def("__getitem__", [](container_type &  self, int64_t index){
            return holder_type(self[index]);
        })
        .def("__setitem__", [](container_type &  self, int64_t index, ptr_type val){
            self[index] = val;
        })


    ;
}

template<class CONTAINER>
void make_set_cls(py::class_<CONTAINER> & py_class)
{
    typedef CONTAINER container_type;
    typedef typename CONTAINER::iterator iterator;
    typedef typename container_type::value_type ptr_type;
    typedef typename std::remove_pointer<ptr_type>::type value_type;
    typedef Holder<value_type> holder_type;

    py_class
        .def("add", [](container_type &  self, ptr_type  val){
            self.insert(val);
        })
        // .def("__getitem__", [](container_type &  self, int64_t index){
        //     return holder_type(self[index]);
        // })
        // .def("__setitem__", [](container_type &  self, int64_t index, ptr_type val){
        //     self[index] = val;
        // })
    ;
}