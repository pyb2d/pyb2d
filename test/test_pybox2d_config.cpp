#include <doctest.h>

#include "pybox2d/pybox2d.hpp"
#include "pybox2d/pybox2d_config.hpp"



TEST_SUITE_BEGIN("core");

TEST_CASE("check version"){

    #ifndef PYBOX2D_VERSION_MAJOR
        #error "PYBOX2D_VERSION_MAJOR is undefined"
    #endif
    

    #ifndef PYBOX2D_VERSION_MINOR
        #error "PYBOX2D_VERSION_MINOR is undefined"
    #endif


    #ifndef PYBOX2D_VERSION_PATCH
        #error "PYBOX2D_VERSION_PATCH is undefined"
    #endif

    CHECK_EQ(PYBOX2D_VERSION_MAJOR , 0);
    CHECK_EQ(PYBOX2D_VERSION_MINOR , 1);
    CHECK_EQ(PYBOX2D_VERSION_PATCH , 0);
}



TEST_SUITE_END(); // end of testsuite core
