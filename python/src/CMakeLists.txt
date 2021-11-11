#-------------------------------------------------------------------------------------------------------------------
# Add The module
#-------------------------------------------------------------------------------------------------------------------
find_package(xtl               REQUIRED)
find_package(xtensor           REQUIRED)
find_package(xtensor-python    CONFIG  REQUIRED)


set(BOX2D_INCLUDE_DIRS 
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/include
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src
)
set(BOX2D_SOURCE_FILES
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_broad_phase.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_chain_shape.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_circle_shape.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_collide_circle.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_collide_edge.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_collide_polygon.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_collision.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_distance.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_dynamic_tree.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_edge_shape.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_polygon_shape.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/collision/b2_time_of_impact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/common/b2_block_allocator.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/common/b2_draw.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/common/b2_math.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/common/b2_settings.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/common/b2_stack_allocator.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/common/b2_timer.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_body.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_chain_circle_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_chain_circle_contact.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_chain_polygon_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_chain_polygon_contact.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_circle_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_circle_contact.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_contact_manager.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_contact_solver.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_contact_solver.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_distance_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_edge_circle_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_edge_circle_contact.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_edge_polygon_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_edge_polygon_contact.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_fixture.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_friction_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_gear_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_island.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_island.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_motor_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_mouse_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_polygon_circle_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_polygon_circle_contact.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_polygon_contact.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_polygon_contact.h
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_prismatic_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_pulley_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_revolute_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_weld_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_wheel_joint.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_world.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/dynamics/b2_world_callbacks.cpp
    ${CMAKE_SOURCE_DIR}/external/box2d-2.4.1/src/rope/b2_rope.cpp
)


set(PY_MOD_NAME pybox2d )
set(PY_MOD_LIB_NAME _${PY_MOD_NAME})





# add the python library
pybind11_add_module(${PY_MOD_LIB_NAME}  
    ${BOX2D_SOURCE_FILES}
    main.cpp
    def_build_config.cpp

    b2Math.cxx
    b2World.cxx
    b2Body.cxx
    b2Fixture.cxx
    b2Shape.cxx
    b2Joint.cxx
    b2JointDef.cxx
    # b2Particle.cxx
    # b2ParticleSystem.cxx
    # b2ParticleGroup.cxx
    # pyEmitter.cxx
    b2WorldCallbacks.cxx
    b2Contact.cxx
    b2Collision.cxx
    b2Draw.cxx
    export_batch_debug_draw.cxx
)



# `link` against pybind11 interface module
target_link_libraries(${PY_MOD_LIB_NAME} PUBLIC  
    ${INTERFACE_LIB_NAME}
    pybind11::module
    xtensor-python)

# include directories for non-modern cmake
set(PY_INCLUDE_DIRS 
    ${PYTHON_NUMPY_INCLUDE_DIR}
    ${BOX2D_INCLUDE_DIRS}
    ${xtensor-python_INCLUDE_DIRS}
)
target_include_directories(${PY_MOD_LIB_NAME} PUBLIC  ${PY_INCLUDE_DIRS})

# custom target for `make python-module`
add_custom_target(python-module DEPENDS ${PY_MOD_LIB_NAME})



add_custom_command(TARGET ${PY_MOD_LIB_NAME} POST_BUILD 
  COMMAND "${CMAKE_COMMAND}" -E copy 
     "$<TARGET_FILE:${PY_MOD_LIB_NAME}>"
     "${CMAKE_BINARY_DIR}/python/module/${PY_MOD_NAME}/$<TARGET_FILE_NAME:${PY_MOD_LIB_NAME}>" 
  COMMENT "Copying to output directory")




add_custom_target(python-test COMMAND ${PYTHON_EXECUTABLE}  -m pytest "${CMAKE_SOURCE_DIR}/python/tests"  WORKING_DIRECTORY "${CMAKE_BINARY_DIR}/python/module" )
add_dependencies(python-test ${PY_MOD_LIB_NAME} )


install(TARGETS ${PY_MOD_LIB_NAME} 
    DESTINATION ${PYTHON_MODULE_INSTALL_DIR}/${PY_MOD_NAME}/)