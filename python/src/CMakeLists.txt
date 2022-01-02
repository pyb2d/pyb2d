#-------------------------------------------------------------------------------------------------------------------
# Add The module
#-------------------------------------------------------------------------------------------------------------------


if(NOT PYBOX2D_LIQUID_FUN)


SET(BOX2D_BASE_DIR ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1)
# SET(BOX2D_BASE_DIR ${CMAKE_SOURCE_DIR}/external/box2d-ecf398ca73f31b282cf9e6a500d8af6665654617)
set(BOX2D_INCLUDE_DIRS
    ${BOX2D_BASE_DIR}/include
    ${BOX2D_BASE_DIR}/src
)

FILE(GLOB_RECURSE BOX2D_SOURCE_FILES ${BOX2D_BASE_DIR}/src/*.cpp)
else()

# SET(BOX2D_BASE_DIR ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1)
SET(BOX2D_BASE_DIR ${CMAKE_SOURCE_DIR}/external/box2d-ecf398ca73f31b282cf9e6a500d8af6665654617)
set(BOX2D_INCLUDE_DIRS
    ${BOX2D_BASE_DIR}/include
    ${BOX2D_BASE_DIR}/src
)

FILE(GLOB_RECURSE BOX2D_SOURCE_FILES ${BOX2D_BASE_DIR}/src/*.cpp)





ENDIF()






if(NOT PYBOX2D_LIQUID_FUN)
    set(LIQUIDFUN_EXTRA_SOURCES "")
else()
    set(LIQUIDFUN_EXTRA_SOURCES
        b2Particle.cxx
        b2ParticleSystem.cxx
        b2ParticleGroup.cxx

        # extensions
        extensions/b2Emitter.cpp
        pyEmitter.cxx
    )
endif()


# add the python library
pybind11_add_module(${PY_MOD_LIB_NAME}
    ${BOX2D_SOURCE_FILES}
    ${LIQUIDFUN_EXTRA_SOURCES}
    b2_user_settings.cpp
    main.cpp
    def_build_config.cpp
    b2Math.cxx
    b2World.cxx
    b2Body.cxx
    b2Fixture.cxx
    b2Shape.cxx
    b2Joint.cxx
    b2JointDef.cxx
    b2WorldCallbacks.cxx
    b2Contact.cxx
    b2Collision.cxx
    b2Draw.cxx
    batch_api.cxx
)



# `link` against pybind11 interface module
target_link_libraries(${PY_MOD_LIB_NAME} PUBLIC
    ${INTERFACE_LIB_NAME}
    pybind11::module)

# include directories for non-modern cmake
set(PY_INCLUDE_DIRS
    ${PYTHON_NUMPY_INCLUDE_DIR}
    ${BOX2D_INCLUDE_DIRS}
)
target_include_directories(${PY_MOD_LIB_NAME} PUBLIC
    ${PY_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}
)
target_compile_definitions(${PY_MOD_LIB_NAME} PUBLIC -DB2_USER_SETTINGS)


if(PYBOX2D_LIQUID_FUN)
    target_compile_definitions(${PY_MOD_LIB_NAME} PUBLIC -DPYBOX2D_LIQUID_FUN)  # -D removed
    # target_compile_definitions(${PY_MOD_LIB_NAME} PUBLIC -DPYBOX2D_OLD_BOX2D)
endif()
target_include_directories(${PY_MOD_LIB_NAME} PUBLIC  ${PY_INCLUDE_DIRS})

# custom target for `make python-module`
add_custom_target(python-module DEPENDS ${PY_MOD_LIB_NAME})



add_custom_command(TARGET ${PY_MOD_LIB_NAME} POST_BUILD
  COMMAND "${CMAKE_COMMAND}" -E copy
     "$<TARGET_FILE:${PY_MOD_LIB_NAME}>"
     "${CMAKE_BINARY_DIR}/python/module/${PY_MOD_NAME}/$<TARGET_FILE_NAME:${PY_MOD_LIB_NAME}>"
  COMMENT "Copying to output directory")




add_custom_target(python-test COMMAND ${PYTHON_EXECUTABLE}  -m pytest "${CMAKE_SOURCE_DIR}/python/tests" -s WORKING_DIRECTORY "${CMAKE_BINARY_DIR}/python/module" )
add_dependencies(python-test ${PY_MOD_LIB_NAME} )


install(TARGETS ${PY_MOD_LIB_NAME}
    DESTINATION ${PYTHON_MODULE_INSTALL_DIR}/${PY_MOD_NAME}/)
