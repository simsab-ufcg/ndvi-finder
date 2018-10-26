#pragma once

#include "types.h"
#include "utils.h"

struct MergeFunction{

    MergeFunction(){};

    ldouble operator()(ldouble first, ldouble second){return NaN;};
};