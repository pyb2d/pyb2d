
#include <iostream>

#include "box2d_wrapper.hpp"
// if either fixture has a groupIndex of zero, use the category/mask rules
// if both groupIndex values are non-zero but different, use the category/mask rules 
// if both groupIndex values are the same and positive, report collision
// if both groupIndex values are the same and negative, don't report collision

bool report_collision(const b2ReportFilter & filterA, const b2ReportFilter & filterB)
{   
    const auto ga = filterA.groupIndex;
    const auto gb = filterB.groupIndex;
    // std::cout<<"ga "<<ga<<" "<<gb<<"\n";
    if((ga == 0 || gb == 0) || (ga != gb))
    {
    return  (filterA.maskBits & filterB.categoryBits) != 0 && (filterA.categoryBits & filterB.maskBits) != 0;
    }
    else { // here ga == gb 
        return ga > 0;
    }
}

