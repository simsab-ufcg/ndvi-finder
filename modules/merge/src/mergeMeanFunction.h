#pragma once

#include "mergeFunction.h"

struct MergeMeanFunction: MergeFunction{

    MergeMeanFunction(): MergeFunction(){};

    ldouble operator() (ldouble first, ldouble second);

};