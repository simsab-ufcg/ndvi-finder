#include "mergeMeanFunction.h"

ldouble MergeMeanFunction::operator() (ldouble first, ldouble second){
    if(isnan(first))
        return second;
    if(isnan(second))
        return first;
    return (first + second) / 2.0;
}
