#pragma once
#ifndef PYBOX2D_PYBOX2D_HPP
#define PYBOX2D_PYBOX2D_HPP

#include <cstdint>
#include <iostream>

namespace pybox2d {
    
    class MyClass
    {
    public:
        MyClass(const uint64_t size)
        : m_size(size)
        {

        }
        
        void hello_world()
        {
            std::cout<<"Hello World!\n";
        }
    private:
        uint64_t m_size;
    };

} // end namespace pybox2d


#endif // PYBOX2D_PYBOX2D_HPP