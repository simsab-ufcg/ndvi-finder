#include "mergePriorityFunction.h"

ldouble MergePriorityFunction::operator() (ldouble first, ldouble second){
    if(!isnan(second))
        return second;
    else
        return first;
}
