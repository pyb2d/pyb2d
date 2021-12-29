#ifndef B2_USER_SETTINGS_HPP
#define B2_USER_SETTINGS_HPP

#include <iostream>

#include <stdarg.h>
#include <stdint.h>
#include <pybind11/pybind11.h>

// Tunable Constants

/// You can use this to change the length scale used by your game.
/// For example for inches you could use 39.4.
#define b2_lengthUnitsPerMeter 1.0f

/// The maximum number of vertices on a convex polygon. You cannot increase
/// this too much because b2BlockAllocator has a maximum object size.
#define b2_maxPolygonVertices   8

// User data

namespace py = pybind11;

// for stupid reasons we cannot reuse b2Filter
struct B2_API b2ReportFilter
{
    b2ReportFilter()
    {
        categoryBits = 0x0001;
        maskBits = 0xFFFF;
        groupIndex = 0;
    }

    /// The collision category bits. Normally you would just set one bit.
    uint16 categoryBits;

    /// The collision mask bits. This states the categories that this
    /// shape would accept for collision.
    uint16 maskBits;

    /// Collision groups allow a certain group of objects to never report collide (negative)
    /// or always collide (positive). Zero means no collision group. Non-zero group
    /// filtering always wins against the mask bits.
    int16 groupIndex;
};



// if either fixture has a groupIndex of zero, use the category/mask rules
// if both groupIndex values are non-zero but different, use the category/mask rules 
// if both groupIndex values are the same and positive, report collision
// if both groupIndex values are the same and negative, don't report collision

B2_API bool report_collision(const b2ReportFilter & filterA, const b2ReportFilter & filterB);
// {   
//     const auto ga = filterA.groupIndex;
//     const auto gb = filterB.groupIndex;
//     std::cout<<"ga "<<ga<<" "<<gb<<"\n";
//     if((ga == 0 || gb == 0) || (ga != gb))
//     {
//         return  (filterA.maskBits & filterB.categoryBits) != 0 && (filterA.categoryBits & filterB.maskBits) != 0;
//     }
//     else { // here ga == gb 
//         return ga > 0;
//     }
// }

struct B2_API UserDataBase
{   
    UserDataBase()
    :   p_object_data(nullptr),
        pointer(0),
        debug_draw(true)
    {
        
    }

    // neither shared nor unique make sense here
    pybind11::object * p_object_data;

    /// For legacy compatibility
    uintptr_t pointer;


    // include in debug draw
    bool debug_draw;
};




struct B2_API ContacReportMixIn
{
    ContacReportMixIn()
    :   reportContactFilter()
    {

    }

    b2ReportFilter reportContactFilter;
};


/// You can define this to inject whatever data you want in b2Body
struct B2_API b2BodyUserData : UserDataBase,ContacReportMixIn
{
    b2BodyUserData()
    :   UserDataBase(),
        ContacReportMixIn()
    {

    }
};

/// You can define this to inject whatever data you want in b2Fixture
struct B2_API b2FixtureUserData : UserDataBase,ContacReportMixIn
{
    b2FixtureUserData()
    :   UserDataBase(),
        ContacReportMixIn()
    {

    }   
};

/// You can define this to inject whatever data you want in b2Joint
struct B2_API b2JointUserData : UserDataBase
{

};

// Memory Allocation

/// Default allocation functions
B2_API void* b2Alloc_Default(int32 size);
B2_API void b2Free_Default(void* mem);

/// Implement this function to use your own memory allocator.
inline void* b2Alloc(int32 size)
{
    return b2Alloc_Default(size);
}

/// If you implement b2Alloc, you should also implement this function.
inline void b2Free(void* mem)
{
    b2Free_Default(mem);
}

/// Use this function to override b2Alloc() without recompiling this library.
typedef void* (*b2AllocFunction)(int32 size, void* callbackData);
/// Use this function to override b2Free() without recompiling this library.
typedef void (*b2FreeFunction)(void* mem, void* callbackData);

/// Set alloc and free callbacks to override the default behavior of using
/// malloc() and free() for dynamic memory allocation.
/// Set allocCallback and freeCallback to nullptr to restore the default
/// allocator (malloc / free).
void b2SetAllocFreeCallbacks(b2AllocFunction allocCallback,
                             b2FreeFunction freeCallback,
                             void* callbackData);

/// Set the number of calls to b2Alloc minus the number of calls to b2Free.
/// This can be used to disable the empty heap check in
/// b2SetAllocFreeCallbacks() which can be useful for testing.
void b2SetNumAllocs(const int32 numAllocs);

/// Get number of calls to b2Alloc minus number of calls to b2Free.
int32 b2GetNumAllocs();

/// Default logging function
B2_API void b2Log_Default(const char* string, va_list args);

/// Implement this to use your own logging.
inline void b2Log(const char* string, ...)
{
    va_list args;
    va_start(args, string);
    b2Log_Default(string, args);
    va_end(args);
}
#endif
