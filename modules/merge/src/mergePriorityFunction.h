#pragma once

#include "mergeFunction.h"

struct MergePriorityFunction: MergeFunction{

    MergePriorityFunction(): MergeFunction(){};

    ldouble operator() (ldouble first, ldouble second);

};