
cmake_minimum_required(VERSION 3.1)
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)
project (pybox2d)


set(PROJECT_INCLUDE_DIR    ${CMAKE_CURRENT_SOURCE_DIR}/include)
set(CPP_ROOT_FOLDER_NAME   pybox2d)
include_directories(${PROJECT_INCLUDE_DIR})

# C++ 14
# ===========
include(CheckCXXCompilerFlag)
if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES "Intel")
    CHECK_CXX_COMPILER_FLAG("-std=c++14" HAS_CPP14_FLAG)
    if (HAS_CPP14_FLAG)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
    else()
        message(FATAL_ERROR "Unsupported compiler -- C++14 support required!")
    endif()
endif()   


# Versionning
# ===========
set(CPP_CONFIG_HEADER_NAME pybox2d_config.hpp)
set(PROJECT_CONFIG_FILE ${PROJECT_INCLUDE_DIR}/${CPP_ROOT_FOLDER_NAME}/${CPP_CONFIG_HEADER_NAME})

file(STRINGS ${PROJECT_CONFIG_FILE} project_version_defines
     REGEX "#define PYBOX2D_VERSION_(MAJOR|MINOR|PATCH)")
message(STATUS ${PROJECT_CONFIG_FILE})

foreach(ver ${project_version_defines})
    if(ver MATCHES "#define PYBOX2D_VERSION_(MAJOR|MINOR|PATCH) +([^ ]+)$")
        set(${PROJECT_NAME}_VERSION_${CMAKE_MATCH_1} "${CMAKE_MATCH_2}" CACHE INTERNAL "")
    endif()
endforeach()

set(${PROJECT_NAME}_VERSION
    ${${PROJECT_NAME}_VERSION_MAJOR}.${${PROJECT_NAME}_VERSION_MINOR}.${${PROJECT_NAME}_VERSION_PATCH})
message(STATUS "Building project v${${PROJECT_NAME}_VERSION}")

# Dependencies
# ============
find_package(xtl      REQUIRED)
find_package(xtensor  REQUIRED)

# # Build
# # =====


SET(INTERFACE_LIB_NAME pybox2d)



file(GLOB_RECURSE ${PROJECT_NAME}_HEADERS  ${PROJECT_INCLUDE_DIR}/*.hpp)


add_library(${INTERFACE_LIB_NAME} INTERFACE)

message(STATUS "INSTALL_INTERFACE: ${CMAKE_INSTALL_INCLUDEDIR}")
target_include_directories(${INTERFACE_LIB_NAME}  INTERFACE 
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)



target_link_libraries(${INTERFACE_LIB_NAME} 
  INTERFACE xtensor)



# Benchmark
# ============
OPTION(BUILD_DOCS "build docs" ON)

OPTION(BUILD_BENCHMARK "${PROJECT_NAME} test suite" OFF)
OPTION(DOWNLOAD_GOOGLE_BENCHMARK "build google benchmark from downloaded sources" OFF)

if(DOWNLOAD_GOOGLE_BENCHMARK)
    set(BUILD_BENCHMARK ON)
endif()

# if(BUILD_BENCHMARK)
#     add_subdirectory(benchmark)
# endif()

# if(BUILD_DOCS)
#     add_subdirectory(docs)
# endif()

# Python
# ============
OPTION(BUILD_PYTHON "${PROJECT_NAME} python binding" ON)
if(BUILD_PYTHON)
    add_subdirectory(python)
    # add_subdirectory(old_python)
endif()



# Tests
###########

OPTION(BUILD_TESTS "${PROJECT_NAME} test suite" ON)
# OPTION(DOWNLOAD_DOCTEST "build doctest from downloaded sources" ON)

# if(DOWNLOAD_DOCTEST)
#     set(BUILD_TESTS ON)
# endif()

if(BUILD_TESTS)
    add_subdirectory(test)
endif()

# Examples
# ============
OPTION(BUILD_EXAMPLES "${PROJECT_NAME} test suite" ON)


if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()



# Installation
# ============

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)


set(${PROJECT_NAME}_CMAKECONFIG_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}" CACHE
    STRING "install path for ${PROJECT_NAME}Config.cmake")


message(STATUS "DEST ${${PROJECT_NAME}_CMAKECONFIG_INSTALL_DIR}" )


install(TARGETS ${INTERFACE_LIB_NAME}
        EXPORT ${INTERFACE_LIB_NAME}-targets)

install(EXPORT ${INTERFACE_LIB_NAME}-targets
        FILE ${INTERFACE_LIB_NAME}Targets.cmake
        #NAMESPACE ${PROJECT_NAME}:: 
        DESTINATION lib/cmake/${PROJECT_NAME}
         )


install(DIRECTORY  ${PROJECT_INCLUDE_DIR}/${CPP_ROOT_FOLDER_NAME}
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})




configure_package_config_file(${PROJECT_NAME}Config.cmake.in
                              "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
                              INSTALL_DESTINATION ${${PROJECT_NAME}_CMAKECONFIG_INSTALL_DIR})


# ${PROJECT_NAME} is header-only and does not depend on the architecture.
# Remove CMAKE_SIZEOF_VOID_P from ${PROJECT_NAME}ConfigVersion.cmake so that an ${PROJECT_NAME}Config.cmake
# generated for a 64 bit target can be used for 32 bit targets and vice versa.
set(_${PROJECT_NAME}_CMAKE_SIZEOF_VOID_P ${CMAKE_SIZEOF_VOID_P})
unset(CMAKE_SIZEOF_VOID_P)
write_basic_package_version_file(${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake
                                 VERSION ${${PROJECT_NAME}_VERSION}
                                 COMPATIBILITY AnyNewerVersion)
set(CMAKE_SIZEOF_VOID_P ${_${PROJECT_NAME}_CMAKE_SIZEOF_VOID_P})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake
              ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake
        DESTINATION ${${PROJECT_NAME}_CMAKECONFIG_INSTALL_DIR})

install(EXPORT ${PROJECT_NAME}-targets
        FILE ${PROJECT_NAME}Targets.cmake
        DESTINATION ${${PROJECT_NAME}_CMAKECONFIG_INSTALL_DIR})

configure_file(${PROJECT_NAME}.pc.in
               "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc"
                @ONLY)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc"
DESTINATION "${CMAKE_INSTALL_LIBDIR}/pkgconfig/")



