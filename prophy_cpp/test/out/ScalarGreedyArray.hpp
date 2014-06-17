#ifndef _PROPHY_GENERATED_ScalarGreedyArray_HPP
#define _PROPHY_GENERATED_ScalarGreedyArray_HPP

#include <prophy/prophy.hpp>

#include "Scalar.hpp"

struct ScalarGreedyArray
{
    uint16_t x;
    uint32_t y[1];
};

namespace prophy
{

inline ScalarGreedyArray* swap(ScalarGreedyArray& payload)
{
    swap(payload.x);
    return cast<ScalarGreedyArray*>(payload.y);
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ScalarGreedyArray_HPP */
